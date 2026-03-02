# app/workers/camera_runtime.py
import os
import threading
import time
import multiprocessing
import re
from datetime import datetime, timedelta
from typing import Any
import pytz

# --- MODULES IMPORTS ---
from app.workers.camera_stream import CameraStream
from app.workers.image_processor import ImageProcessor
from app.workers.video_recorder import VideoRecorder
from app.workers.packing_machine import PackingStateMachine, MachineState, Action
from app.services.order_repository import order_repo
from app.services.media_service import media_service
from app.core.resolution_loader import get_system_resolution
from app.core.oc_enums import OrderStatus, OrderNote
from app.crud.setting_crud import setting as setting_crud
from app.db.session import SessionLocal
from app.services.google_tts import tts_service
from app.services.socket_service import socket_service
from app.services.carrier_service import carrier_service

from sqlalchemy import func, distinct
from app.db import models 

os.environ["OPENCV_LOG_LEVEL"] = "OFF"
RECONNECT_DELAY = 5.0

def validate_shipping_code(code: str) -> bool:
    if not code: return False
    code = str(code).upper().strip()
    if len(code) <= 5: return False
    if not re.match(r'^[A-Z0-9\.]+$', code): return False
    patterns = [
        r'^SPX', r'^VN[0-9A-Z]+', r'^[0-9]{9,15}$', 
        r'^[A-Z]{2}[0-9]{9}[A-Z]{2}$', r'^[A-Z0-9]{8,20}$', 
        r'^84[0-9]+', r'^TE[0-9]+', r'^S\d+\.'
    ]
    for pattern in patterns:
        if re.search(pattern, code): return True
    return False

class CameraRuntime:
    def __init__(self, cam_id: int, source: Any, ai_queue: multiprocessing.Queue):
        self.cam_id = cam_id
        self.ai_queue = ai_queue
        self.current_avatar_path = None 
        
        self.target_w, self.target_h = 854, 480 
        self.fps_record = 10.0
        self.fps_view_limit = 15.0
        self.ai_interval = 3
        self.enable_audio = True
        
        self.stream = CameraStream(source, cam_id)
        self.img_proc = ImageProcessor()
        self.machine = PackingStateMachine()
        
        self._load_and_apply_settings()
        print(f"🔧 [Cam {cam_id}] Stream/UI Target Resolution: {self.target_w}x{self.target_h}")

        self.recorder = VideoRecorder(fps=self.fps_record) 

        self.is_running = False
        self.is_connected = False
        self.thread = None
        self.lock = threading.Lock()
        
        self.jpeg_bytes = None
        self.raw_frame_for_ai = None
        self.ai_metadata = [] 
        self.stream_metadata = {} 
        self.last_scanned_code = None
        self.last_scanned_time = 0
        
        self.current_order_db_id = None
        self.rec_start_time = 0
        self.code_context_cache = {}
        
        self.stop_deadline = 0.0
        self.pending_stop_data = None
        
        self.last_scan_audio_time = 0
        self.SCAN_AUDIO_COOLDOWN = 3.0
        self.read_end_digits_count = 5
        self.last_spoken_code = None
        self.last_code_speak_time = 0 

        self.start()

    @property
    def recording(self) -> bool:
        return (self.machine.state == MachineState.PACKING) or (self.stop_deadline > 0)

    def _emit_event(self, event_name, data):
        self.stream_metadata = {
            "event": event_name, "data": data, "ts": time.time()
        }
        if event_name in ["ORDER_CREATED", "ORDER_STOPPED", "ORDER_UPDATED"]:
            try:
                payload = data.copy() if isinstance(data, dict) else {}
                payload['cam_id'] = self.cam_id
                socket_service.broadcast_event(event_name, payload)
            except Exception as e: pass

    def _load_and_apply_settings(self):
            try:
                db = SessionLocal()
                settings = setting_crud.get_all_as_dict(db)
                db.close()
                
                try:
                    db_w = int(settings.get("camera_width", "854"))
                    db_h = int(settings.get("camera_height", "480"))
                    self.target_w, self.target_h = db_w, db_h
                except ValueError:
                    self.target_w, self.target_h = 854, 480
                
                timeout = int(settings.get("timeout_no_human", "60"))
                end_time = settings.get("work_end_time", "18:30")
                self.read_end_digits_count = int(settings.get("read_end_order", "5"))
                self.machine.update_config(timeout, end_time)

                self.fps_record = float(settings.get("perf_record_fps", "10.0"))
                self.fps_view_limit = float(settings.get("perf_view_fps", "15.0"))
                
                self.ai_interval = int(settings.get("perf_ai_interval", "3"))
                if self.ai_interval <= 0:
                    self.ai_interval = 3
                    
                self.enable_audio = str(settings.get("enable_audio", "true")).lower() == "true"
                    
            except Exception as e: pass

    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread: self.thread.join(timeout=2.0)
        self._do_stop_order(self.machine.current_code, OrderNote.SYSTEM_RESTART)
        with self.lock: self.is_connected = False

    def start_recording(self, code):
        self.stop_deadline = 0 
        self.pending_stop_data = None
        if self.machine.force_start(code) == Action.START_ORDER:
            self._do_start_order(code, note=OrderNote.MANUAL)

    def stop_recording(self):
        self.stop_deadline = 0
        self.pending_stop_data = None
        action, code = self.machine.manual_stop()
        if action == Action.STOP_ORDER:
            self._do_stop_order(code, OrderNote.MANUAL)

    def get_jpeg(self):
        with self.lock: return self.jpeg_bytes

    def get_snapshot(self):
        with self.lock:
            if self.raw_frame_for_ai is None: return None
            return self.img_proc.to_jpeg(self.raw_frame_for_ai)

    def _safe_speak(self, text):
        if not self.enable_audio: return
        try:
            if text:
                tts_service.speak(text)
        except Exception as e: pass

    def _do_start_order(self, code, parent_id=None, note=None):
        if not code: return
        try:
            if self.stop_deadline > 0 and self.pending_stop_data:
                old_code, old_reason = self.pending_stop_data
                self._do_stop_order(old_code, old_reason)
                self.stop_deadline = 0
                self.pending_stop_data = None

            print(f"🟢 START REC: {code}")
            self.current_avatar_path = None 
            self.recorder.start(code, self.target_w, self.target_h)
            
            self.current_order_db_id = order_repo.create_order(
                code=code, cam_id=self.cam_id, parent_id=parent_id, note=note
            )
            self.rec_start_time = time.time()
            final_note = note or (OrderNote.REPACK if parent_id else OrderNote.NEW_ORDER)
            
            if note:
                def _speak_note_delayed(note_text):
                    try:
                        time.sleep(2.0)
                        self._safe_speak(note_text)
                    except: pass
                threading.Thread(target=_speak_note_delayed, args=(final_note,), daemon=True).start()

            self._emit_event("ORDER_CREATED", {
                "code": code, "status": OrderStatus.PACKING, 
                "note": final_note, "start_time": self.rec_start_time * 1000,
                "order_id": self.current_order_db_id
            })
        except Exception as e: pass

    def _do_stop_order(self, code, reason):
        print(f"⚪ STOP REC: {code} ({reason})")
        closing_order_id = self.current_order_db_id
        video_path = self.recorder.stop()
        
        if self.current_order_db_id:
            if reason == OrderNote.CHECKING_ONLY:
                order_repo.cancel_order(self.current_order_db_id)
            else:
                order_repo.close_order(self.current_order_db_id, reason)
        
        if video_path and os.path.exists(video_path):
            vn_time = datetime.utcnow() + timedelta(hours=7)
            media_service.queue_video_conversion(video_path, code, vn_time, self.current_order_db_id)
        
        if reason not in [OrderNote.CHECKING_ONLY, OrderNote.SYSTEM_RESTART]:
            try:
                tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')
                now_vn = datetime.now(tz_vn)
                start_naive = now_vn.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
                end_naive = now_vn.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=None)
                
                with SessionLocal() as db:
                    count = db.query(func.count(distinct(models.Order.code))).filter(
                        models.Order.status == OrderStatus.CLOSED,
                        models.Order.created_at >= start_naive,
                        models.Order.created_at <= end_naive
                    ).scalar()
                
                if count:
                    self._safe_speak(f"Đã làm xong {count} đơn hôm nay")
            except Exception as e: pass

        self._emit_event("ORDER_STOPPED", {
            "code": code, 
            "note": reason,
            "order_id": closing_order_id 
        })
        
        self.current_order_db_id = None
        self.current_avatar_path = None
        self.last_spoken_code = None

    def _do_snapshot(self, frame, code):
        try:
            path = self.recorder.snapshot(frame, code)
            if path:
                self.current_avatar_path = path 
                if self.current_order_db_id:
                    order_repo.update_avatar(self.current_order_db_id, path)
                    self._emit_event("ORDER_UPDATED", {"order_id": self.current_order_db_id, "path_avatar": path})
        except: pass

    def _capture_loop(self):
        print(f"📷 [Cam {self.cam_id}] Loop Started.")
        while self.is_running:
            try:
                hw_w, hw_h = 640, 480
                target_ratio = self.target_w / self.target_h if self.target_h > 0 else 1.33
                if self.target_w >= 1280 or target_ratio > 1.5:
                    hw_w, hw_h = 1280, 720
                
                if not self.stream.connect(hw_w, hw_h):
                    time.sleep(RECONNECT_DELAY)
                    continue
                
                with self.lock: self.is_connected = True
                frame_cnt = 0
                err_cnt = 0
                last_frame_time = time.time()

                while self.is_running:
                    # [QUAN TRỌNG NHẤT]: Trả CPU về cho hệ điều hành trong 5 mili-giây để Web/Socket không bị chết
                    time.sleep(0.005) 

                    ret, raw_frame = self.stream.read()
                    if not ret:
                        err_cnt += 1
                        time.sleep(0.05)
                        if err_cnt > 30: 
                            print(f"🔄 [Cam {self.cam_id}] Mất luồng hình ảnh. Đang tự động kết nối lại...")
                            break 
                        continue
                    err_cnt = 0

                    now = time.time()
                    target_delay = 1.0 / self.fps_view_limit if self.fps_view_limit > 0 else 0.033
                    
                    if now - last_frame_time < target_delay:
                        # Vẫn nhường thêm CPU nếu Camera đọc quá nhanh
                        time.sleep(0.002) 
                        continue
                        
                    last_frame_time = now

                    frame = self.img_proc.smart_resize(raw_frame, self.target_w, self.target_h)
                    if frame is None: continue

                    frame_cnt += 1
                    if frame_cnt % self.ai_interval == 0:
                        try:
                            if not self.ai_queue.full():
                                ai_input = self.img_proc.preprocess_for_ai(frame)
                                self.ai_queue.put_nowait({
                                    "cam_id": self.cam_id, "image": ai_input,
                                    "target_w": self.target_w, "target_h": self.target_h
                                })
                        except: pass

                    self._process_logic(now, frame)
                    self._draw_overlay(frame)

                    if self.machine.state == MachineState.PACKING or self.stop_deadline > 0:
                        self.recorder.write_frame(frame)

                    jpeg = self.img_proc.to_jpeg(frame)
                    if jpeg:
                        with self.lock:
                            self.jpeg_bytes = jpeg
                            self.raw_frame_for_ai = frame 

            except Exception as e:
                time.sleep(1.0)
            finally:
                self.stream.release()
                with self.lock: self.is_connected = False

    def _process_logic(self, now, frame):
        if self.stop_deadline > 0:
            if now >= self.stop_deadline:
                if self.pending_stop_data:
                    c, r = self.pending_stop_data
                    self._do_stop_order(c, r)
                self.stop_deadline = 0
                self.pending_stop_data = None

        meta = list(self.ai_metadata)
        
        raw_codes = [m['code'] for m in meta if m['type'] in ['qrcode','code']]
        final_codes = []
        for c in raw_codes:
            c_clean = str(c).upper().strip()
            if validate_shipping_code(c_clean):
                final_codes.append(c_clean)

        human = any(m['type'] == 'human' for m in meta)
        if final_codes: human = True

        if final_codes:
            current_code = final_codes[0]
            self.last_scanned_code = current_code
            self.last_scanned_time = now
            
            if current_code != self.last_spoken_code:
                if now - self.last_scan_audio_time > self.SCAN_AUDIO_COOLDOWN:
                    n = self.read_end_digits_count
                    carrier_service.detect_and_speak(current_code, n)
                    
                    self.last_spoken_code = current_code
                    self.last_scan_audio_time = now
                    self.last_code_speak_time = now

        codes_for_machine = final_codes
        
        if self.machine.state == MachineState.IDLE and final_codes:
            code = final_codes[0]
            cache = self.code_context_cache.get(code)
            if not cache or (now - cache['ts'] > 600):
                ord_obj = order_repo.get_latest_order_by_code(code)
                is_old, pid = False, None
                if ord_obj:
                    diff = datetime.now() - ord_obj.created_at
                    if diff.days < 4:
                        is_old = True
                        pid = ord_obj.parent_id if ord_obj.parent_id else ord_obj.id
                cache = {'is_old': is_old, 'pid': pid, 'ts': now}
                self.code_context_cache[code] = cache
            
            if cache['is_old']:
                if self.machine.force_start(code) == Action.START_ORDER:
                    self._do_start_order(code, parent_id=cache['pid'], note=OrderNote.REPACK)
                    codes_for_machine = []

        state, action, code, reason = self.machine.process(codes_for_machine, human)

        if action == Action.START_ORDER:
            self._do_start_order(code, note=OrderNote.NEW_ORDER)
            
        elif action == Action.STOP_ORDER:
            note = OrderNote.MANUAL
            if reason == "TIMEOUT": note = OrderNote.TIMEOUT
            elif reason == "END_SHIFT": note = OrderNote.END_SHIFT
            self.stop_deadline = now + 5.0
            self.pending_stop_data = (code, note)
            
        elif action == Action.SNAPSHOT:
            self._do_snapshot(frame, code)
            
        elif action == Action.SWITCH_ORDER:
            if self.stop_deadline > 0 and self.pending_stop_data:
                 old_c, old_r = self.pending_stop_data
                 self._do_stop_order(old_c, old_r)
                 self.stop_deadline = 0
                 self.pending_stop_data = None
            else:
                 self._do_stop_order(self.machine.last_closed_code, OrderNote.SCAN_NEW)
            
            time.sleep(0.1) 
            self._do_start_order(code, note=OrderNote.NEW_ORDER)

        if state == MachineState.PACKING:
            dur = now - self.machine.packing_start_time
            if 5.5 < dur < 6.5:
                silence = now - self.machine.last_human_seen_time
                if silence > 5.0:
                    self.machine.state = MachineState.IDLE
                    self.machine.current_code = None
                    self._do_stop_order(code, OrderNote.CHECKING_ONLY)

    def _draw_overlay(self, frame):
            state = self.machine.state
            # Kéo text xuống một chút (từ 25 -> 35) để chữ to không bị lẹm viền trên
            base_y = 35 
            
            if state == MachineState.PACKING and self.machine.current_code:
                # Mã đơn hàng: Chữ to (0.8), in đậm (thickness=2)
                self.img_proc.draw_text(frame, self.machine.current_code, 20, base_y, (59, 245, 140), scale=0.8, thickness=2)
                # Trạng thái PACKING: Chữ vừa (0.5), in đậm (thickness=2), đẩy xuống dòng dưới
                self.img_proc.draw_text(frame, "PACKING", 20, base_y + 30, (238, 245, 39), scale=0.5, thickness=2)
                
            elif self.stop_deadline > 0:
                remain = int(max(0, self.stop_deadline - time.time()))
                text = f"FINISHING... {remain}s"
                # Chữ to, in đậm
                self.img_proc.draw_text(frame, text, 20, base_y, (0, 165, 255), scale=0.8, thickness=2)
                
            elif self.last_scanned_code and (time.time() - self.last_scanned_time < 2.0):
                text = f"DETECTED: {self.last_scanned_code}"
                # Chữ to, in đậm
                self.img_proc.draw_text(frame, text, 20, base_y, (0, 255, 255), scale=0.8, thickness=2)
                
            # Hiển thị thời gian (Góc phải)
            try:
                tz = pytz.timezone('Asia/Ho_Chi_Minh')
                now_s = datetime.now(tz).strftime("%d/%m/%Y %I:%M:%S %p")
                # Trừ hao 300px để chữ to không bị tràn ra ngoài lề phải
                self.img_proc.draw_text(frame, now_s, self.target_w - 300, base_y, (255, 255, 255), scale=0.6, thickness=2)
            except:
                now_s = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.img_proc.draw_text(frame, now_s, self.target_w - 250, base_y, (255, 255, 255), scale=0.6, thickness=2)