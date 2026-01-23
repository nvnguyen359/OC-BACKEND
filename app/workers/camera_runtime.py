# app/workers/camera_runtime.py
import os
import threading
import time
import multiprocessing
import platform
from datetime import datetime, timedelta, date
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

# [QUAN TRỌNG] Import để query đếm số đơn
from sqlalchemy import func, distinct
from app.db import models 

# --- CẤU HÌNH CỤC BỘ ---
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
FPS_RECORD = 20.0
RECONNECT_DELAY = 5.0

class CameraRuntime:
    def __init__(self, cam_id: int, source: Any, ai_queue: multiprocessing.Queue):
        self.cam_id = cam_id
        self.ai_queue = ai_queue
        
        self.current_avatar_path = None 
        
        # 1. Load Cấu hình
        self.target_w, self.target_h = get_system_resolution()
        print(f"🔧 [Cam {cam_id}] Target Res: {self.target_w}x{self.target_h}")

        # 2. Modules con
        self.stream = CameraStream(source, cam_id)
        self.img_proc = ImageProcessor()
        self.recorder = VideoRecorder(fps=FPS_RECORD)
        self.machine = PackingStateMachine()

        # 3. Trạng thái
        self.is_running = False
        self.is_connected = False
        self.thread = None
        self.lock = threading.Lock()
        
        # Dữ liệu ảnh
        self.jpeg_bytes = None
        self.raw_frame_for_ai = None
        self.ai_metadata = [] 
        
        # Biến metadata
        self.stream_metadata = {} 
        self.last_scanned_code = None
        self.last_scanned_time = 0
        
        # Dữ liệu Đơn hàng
        self.current_order_db_id = None
        self.rec_start_time = 0
        self.code_context_cache = {}
        
        # Biến xử lý Stop Delay
        self.stop_deadline = 0.0     # Thời điểm sẽ thực sự dừng
        self.pending_stop_data = None # Dữ liệu (code, reason) để dừng sau 5s
        
        # Audio Cooldown
        self.last_scan_audio_time = 0
        self.SCAN_AUDIO_COOLDOWN = 3.0

        # TTS Config
        self.read_end_digits_count = 5
        self.last_spoken_code = None
        self.last_code_speak_time = 0 # [NEW] Thời điểm đọc mã đơn gần nhất

        self._load_and_apply_settings()
        self.start()

    @property
    def recording(self) -> bool:
        # Đang quay nếu Machine Packing HOẶC đang trong thời gian chờ dừng (Delay 5s)
        return (self.machine.state == MachineState.PACKING) or (self.stop_deadline > 0)

    def _emit_event(self, event_name, data):
        self.stream_metadata = {
            "event": event_name,
            "data": data,
            "ts": time.time()
        }

        if event_name in ["ORDER_CREATED", "ORDER_STOPPED", "ORDER_UPDATED"]:
            try:
                payload = data.copy() if isinstance(data, dict) else {}
                payload['cam_id'] = self.cam_id
                socket_service.broadcast_event(event_name, payload)
            except Exception as e:
                print(f"⚠️ [Socket Error] {e}")

    def _load_and_apply_settings(self):
        try:
            db = SessionLocal()
            settings = setting_crud.get_all_as_dict(db)
            db.close()
            timeout = int(settings.get("timeout_no_human", "60"))
            end_time = settings.get("work_end_time", "18:30")
            self.read_end_digits_count = int(settings.get("read_end_order", "5"))
            
            self.machine.update_config(timeout, end_time)
        except Exception: pass

    # --- CONTROL ---
    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread: self.thread.join(timeout=2.0)
        # Force stop ngay lập tức, không delay
        self._do_stop_order(self.machine.current_code, OrderNote.SYSTEM_RESTART)
        self.stream.release()
        with self.lock: self.is_connected = False

    def start_recording(self, code):
        print(f"🔴 Force Start: {code}")
        # Reset delay stop nếu có
        self.stop_deadline = 0 
        self.pending_stop_data = None
        
        if self.machine.force_start(code) == Action.START_ORDER:
            self._do_start_order(code, note=OrderNote.MANUAL)

    def stop_recording(self):
        print(f"⚪ Force Stop")
        # Reset delay stop để dừng ngay
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

    # --- NGHIỆP VỤ ---
    def _do_start_order(self, code, parent_id=None, note=None):
        if not code: return
        try:
            # Nếu đang chờ dừng đơn cũ -> Dừng ngay lập tức để bắt đầu đơn mới
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
            
            # [TTS LOGIC MỚI] Đọc Note có delay theo thứ tự: Code -> 2s -> Note
            if note:
                def _speak_note_delayed(note_text):
                    # Thời gian dự kiến đọc xong mã đơn = last_code_speak_time + 3.5s (ước lượng)
                    # Thời gian cần phát Note = thời gian đọc xong + 2.0s delay
                    
                    gap_delay = 2.0
                    estimated_read_time = 3.5
                    
                    time_since_code = time.time() - self.last_code_speak_time
                    
                    # Nếu vừa mới đọc code (trong vòng 6s), thì chờ cho hết code + gap
                    if time_since_code < (estimated_read_time + gap_delay):
                        wait_time = (estimated_read_time + gap_delay) - time_since_code
                        if wait_time > 0:
                            time.sleep(wait_time)
                            
                    # Thực hiện đọc
                    tts_service.speak(note_text)

                # Chạy thread delay để không chặn luồng quay video
                threading.Thread(target=_speak_note_delayed, args=(final_note,), daemon=True).start()

            self._emit_event("ORDER_CREATED", {
                "code": code, 
                "status": OrderStatus.PACKING, 
                "note": final_note, 
                "start_time": self.rec_start_time * 1000,
                "order_id": self.current_order_db_id
            })
        except Exception as e: print(f"❌ Start Err: {e}")

    def _do_stop_order(self, code, reason):
        print(f"⚪ STOP REC: {code} ({reason})")
        video_path = self.recorder.stop()
        if self.current_order_db_id:
            if reason == OrderNote.CHECKING_ONLY:
                order_repo.cancel_order(self.current_order_db_id)
            else:
                order_repo.close_order(self.current_order_db_id, reason)
        
        if video_path and os.path.exists(video_path):
            vn_time = datetime.utcnow() + timedelta(hours=7)
            media_service.queue_video_conversion(video_path, code, vn_time, self.current_order_db_id)
        
        # [TTS LOGIC] Đếm số đơn hoàn thành trong ngày
        if reason not in [OrderNote.CHECKING_ONLY, OrderNote.SYSTEM_RESTART]:
            try:
                tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')
                now_vn = datetime.now(tz_vn)
                start_of_day = now_vn.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = now_vn.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                start_naive = start_of_day.replace(tzinfo=None)
                end_naive = end_of_day.replace(tzinfo=None)
                
                with SessionLocal() as db:
                    count = db.query(func.count(distinct(models.Order.code))).filter(
                        models.Order.status == OrderStatus.CLOSED,
                        models.Order.created_at >= start_naive,
                        models.Order.created_at <= end_naive
                    ).scalar()
                
                if count:
                    msg = f"Đã làm xong {count} đơn hôm nay"
                    tts_service.speak(msg)
            except Exception as e:
                print(f"❌ TTS Count Error: {e}")

        self._emit_event("ORDER_STOPPED", {"code": code, "note": reason})
        
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

    # --- MAIN LOOP ---
    def _capture_loop(self):
        print(f"📷 [Cam {self.cam_id}] Loop Started (Background Mode)")
        while self.is_running:
            if not self.stream.connect(self.target_w, self.target_h):
                if not hasattr(self, '_log_debounce') or time.time() - self._log_debounce > 10:
                    print(f"⚠️ [Cam {self.cam_id}] Waiting for signal...")
                    self._log_debounce = time.time()
                with self.lock: self.is_connected = False
                time.sleep(RECONNECT_DELAY)
                continue
            
            print(f"✅ [Cam {self.cam_id}] Connected & Processing.")
            with self.lock: self.is_connected = True
            
            frame_cnt = 0
            err_cnt = 0
            while self.is_running:
                ret, raw_frame = self.stream.read()
                now = time.time()
                if not ret:
                    err_cnt += 1
                    time.sleep(0.05)
                    if err_cnt > 30: break 
                    continue
                err_cnt = 0

                frame = self.img_proc.smart_resize(raw_frame, self.target_w, self.target_h)
                if frame is None: continue

                frame_cnt += 1
                if frame_cnt % 5 == 0:
                    try:
                        ai_input = self.img_proc.preprocess_for_ai(frame)
                        self.ai_queue.put_nowait({
                            "cam_id": self.cam_id, "image": ai_input,
                            "target_w": self.target_w, "target_h": self.target_h
                        })
                    except: pass

                self._process_logic(now, frame)
                self._draw_overlay(frame)

                # [UPDATE] Ghi hình nếu đang PACKING hoặc đang trong thời gian Delay Stop
                if self.machine.state == MachineState.PACKING or self.stop_deadline > 0:
                    self.recorder.write_frame(frame)

                jpeg = self.img_proc.to_jpeg(frame)
                if jpeg:
                    with self.lock:
                        self.jpeg_bytes = jpeg
                        self.raw_frame_for_ai = frame 
                time.sleep(0.001)
            self.stream.release()

    def _process_logic(self, now, frame):
        # 1. Check Pending Stop Delay
        if self.stop_deadline > 0:
            if now >= self.stop_deadline:
                # Hết giờ delay 5s -> Thực hiện dừng thật
                if self.pending_stop_data:
                    c, r = self.pending_stop_data
                    self._do_stop_order(c, r)
                self.stop_deadline = 0
                self.pending_stop_data = None

        meta = list(self.ai_metadata)
        final_codes = [m['code'] for m in meta if m['type'] in ['qrcode','code']]
        human = any(m['type'] == 'human' for m in meta)
        if final_codes: human = True

        if final_codes:
            current_code = final_codes[0]
            self.last_scanned_code = current_code
            self.last_scanned_time = now
            if now - self.last_scan_audio_time > self.SCAN_AUDIO_COOLDOWN:
                self.last_scan_audio_time = now
            
            # [TTS] Đọc mã đơn
            if current_code != self.last_spoken_code:
                n = self.read_end_digits_count
                text_to_read = current_code[-n:] if len(current_code) > n else current_code
                tts_service.speak(f"mã đơn {n} số cuối {text_to_read}")
                
                self.last_spoken_code = current_code
                self.last_code_speak_time = time.time() # [NEW] Ghi lại thời điểm đọc code

        codes_for_machine = final_codes
        
        # 2. Xử lý DB Check (Check 4 Ngày)
        if self.machine.state == MachineState.IDLE and final_codes:
            code = final_codes[0]
            cache = self.code_context_cache.get(code)
            
            # Cache 10 phút để tránh query DB liên tục
            if not cache or (now - cache['ts'] > 600):
                ord_obj = order_repo.get_latest_order_by_code(code)
                is_old = False
                pid = None
                
                if ord_obj:
                    # [FIX Logic] Check khoảng cách ngày
                    # < 4 ngày: Repack (Đóng thêm/bớt hàng) -> Nối parent_id
                    # >= 4 ngày: Đơn hoàn (Return) -> Coi như đơn mới
                    diff = datetime.now() - ord_obj.created_at
                    if diff.days < 4:
                        is_old = True
                        pid = ord_obj.parent_id if ord_obj.parent_id else ord_obj.id
                
                cache = {'is_old': is_old, 'pid': pid, 'ts': now}
                self.code_context_cache[code] = cache
            
            if cache['is_old']:
                # Nếu là đơn Repack (<4 ngày) -> Nối tiếp (Start luôn, bỏ qua delay stop nếu có)
                if self.machine.force_start(code) == Action.START_ORDER:
                    self._do_start_order(code, parent_id=cache['pid'], note=OrderNote.REPACK)
                    codes_for_machine = []

        # 3. State Machine Process
        state, action, code, reason = self.machine.process(codes_for_machine, human)

        if action == Action.START_ORDER:
            # Code mới -> Start luôn
            self._do_start_order(code, note=OrderNote.NEW_ORDER)
            
        elif action == Action.STOP_ORDER:
            # Dừng đơn -> Kích hoạt Delay 5s
            note = OrderNote.MANUAL
            if reason == "TIMEOUT": note = OrderNote.TIMEOUT
            elif reason == "END_SHIFT": note = OrderNote.END_SHIFT
            
            print(f"⏳ Trigger Delayed Stop for {code} (5s)...")
            self.stop_deadline = now + 5.0
            self.pending_stop_data = (code, note)
            
        elif action == Action.SNAPSHOT:
            self._do_snapshot(frame, code)
            
        elif action == Action.SWITCH_ORDER:
            # Chuyển đơn -> Dừng ngay đơn cũ, Start đơn mới
            if self.stop_deadline > 0 and self.pending_stop_data:
                 old_c, old_r = self.pending_stop_data
                 self._do_stop_order(old_c, old_r)
                 self.stop_deadline = 0
                 self.pending_stop_data = None
            else:
                 self._do_stop_order(self.machine.last_closed_code, OrderNote.SCAN_NEW)

            self._do_start_order(code, note=OrderNote.NEW_ORDER)

        if state == MachineState.PACKING:
            dur = now - self.machine.packing_start_time
            if 5.5 < dur < 6.5:
                silence = now - self.machine.last_human_seen_time
                if silence > 5.0:
                    print(f"⚠️ C4: No human {silence:.1f}s -> Cancel")
                    self.machine.state = MachineState.IDLE
                    self.machine.current_code = None
                    self._do_stop_order(code, OrderNote.CHECKING_ONLY)

    def _draw_overlay(self, frame):
        state = self.machine.state
        
        # Hiển thị trạng thái
        if state == MachineState.PACKING and self.machine.current_code:
            text = f"PACKING: {self.machine.current_code}"
            self.img_proc.draw_text(frame, text, 20, 50, (0, 255, 0))
        elif self.stop_deadline > 0:
            remain = max(0, self.stop_deadline - time.time())
            text = f"FINISHING... {remain:.1f}s"
            self.img_proc.draw_text(frame, text, 20, 50, (0, 165, 255))
        elif self.last_scanned_code and (time.time() - self.last_scanned_time < 2.0):
            text = f"DETECTED: {self.last_scanned_code}"
            self.img_proc.draw_text(frame, text, 20, 50, (0, 255, 255))
            
        try:
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now_s = datetime.now(tz).strftime("%d/%m/%Y %I:%M:%S %p")
            self.img_proc.draw_text(frame, now_s, self.target_w - 360, 50, (255, 255, 255))
        except:
            now_s = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.img_proc.draw_text(frame, now_s, self.target_w - 280, 50, (255, 255, 255))