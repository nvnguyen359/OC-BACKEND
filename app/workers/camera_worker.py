# app/workers/camera_worker.py
import os
import sys

# 1. Cấu hình môi trường
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_OBSENSOR"] = "0"

import threading
import time
import cv2
import multiprocessing
import queue
import platform
import signal
import psutil
from datetime import datetime
from typing import Dict, Optional, Any
from app.workers.ai_detector import run_ai_process

# [CHUẨN HÓA] Thống nhất độ phân giải 16:9 (HD 720p)
# Tỉ lệ này hiển thị tốt nhất trên cả Mobile & Desktop
TARGET_WIDTH = 1280 
TARGET_HEIGHT = 720 

# --- HELPER VẼ (TEXT TRẮNG VIỀN ĐEN) ---
def put_text_with_outline(img, text, x, y, font_scale, thickness, color=(255, 255, 255)):
    """
    Vẽ chữ màu Trắng, viền Đen để nổi bật trên mọi nền.
    """
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 1. Vẽ viền đen (dày hơn lõi 3px)
        cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
        # 2. Vẽ lõi màu (Mặc định Trắng)
        cv2.putText(img, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
    except: pass

# --- HELPER CHẶN LOG C++ ---
class FailsafeSuppressStderr:
    def __enter__(self):
        try:
            sys.stderr.flush()
            self.devnull = os.open(os.devnull, os.O_RDWR)
            self.saved_stderr = os.dup(sys.stderr.fileno())
            os.dup2(self.devnull, sys.stderr.fileno())
        except: pass
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            os.dup2(self.saved_stderr, sys.stderr.fileno())
            os.close(self.devnull)
        except: pass

# --- CAMERA RUNTIME ---
class CameraRuntime:
    def __init__(self, cam_id: int, source: Any, ai_queue: multiprocessing.Queue):
        self.cam_id = cam_id
        self.source = source
        self.ai_queue = ai_queue
        
        self.is_running = False
        self.thread = None
        
        self.jpeg_bytes: Optional[bytes] = None 
        self.raw_frame_for_ai: Optional[Any] = None 
        
        self.lock = threading.Lock()
        
        # Metadata từ AI
        self.ai_metadata = [] 
        
        # Trạng thái ghi hình
        self.recording = False
        self.order_code = None
        
        self.start()

    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        with self.lock:
            self.jpeg_bytes = None

    def start_recording(self, order_code: str):
        print(f"🔴 [Cam {self.cam_id}] START RECORD")
        with self.lock:
            self.recording = True
            if order_code and order_code != "MANUAL":
                self.order_code = order_code

    def stop_recording(self):
        print(f"⚪ [Cam {self.cam_id}] STOP RECORD")
        with self.lock:
            self.recording = False

    def _capture_loop(self):
        src = self.source
        if isinstance(src, str) and src.isdigit(): src = int(src)
        print(f"📷 [System] Starting Cam {self.cam_id}")

        # --- MỞ CAMERA ---
        cap = None
        if isinstance(src, int) and platform.system() == 'Windows':
            with FailsafeSuppressStderr():
                cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
            try: 
                # Cố gắng set phần cứng về 1280x720 trước
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*'MJPG'))
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, TARGET_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, TARGET_HEIGHT)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except: pass
        else:
            with FailsafeSuppressStderr():
                cap = cv2.VideoCapture(src)
            
        if not cap or not cap.isOpened():
            print(f"❌ [System] Failed Cam {self.cam_id}")
            self.is_running = False
            return
        
        print(f"✅ [System] Cam {self.cam_id} Running.")
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        frame_cnt = 0

        while self.is_running:
            ret, raw_frame = cap.read()
            if ret:
                # [QUAN TRỌNG] Chuẩn hóa kích thước
                h, w = raw_frame.shape[:2]
                
                # Kiểm tra cả CHIỀU RỘNG và CHIỀU CAO
                if w != TARGET_WIDTH or h != TARGET_HEIGHT:
                    # Ép về 1280x720 (có thể bị méo nhẹ nếu nguồn là 4:3, nhưng đảm bảo giao diện đẹp)
                    resized = cv2.resize(raw_frame, (TARGET_WIDTH, TARGET_HEIGHT), interpolation=cv2.INTER_LINEAR)
                else:
                    resized = raw_frame

                # === 1. AUTO-SYNC CODE TỪ AI ===
                if self.ai_metadata:
                    for obj in self.ai_metadata:
                        ai_code = obj.get("code")
                        if ai_code:
                            self.order_code = ai_code
                            break

                # === 2. CẤU HÌNH VẼ (TRẮNG VIỀN ĐEN) ===
                COMMON_FONT_SCALE = 0.85
                COMMON_THICKNESS = 2
                TEXT_COLOR = (255, 255, 255)
                
                # === 3. VẼ OVERLAY ===
                
                # A. Mã đơn (Góc TRÊN TRÁI)
                if self.order_code:
                    put_text_with_outline(resized, str(self.order_code), 20, 40, 
                                          COMMON_FONT_SCALE, COMMON_THICKNESS, TEXT_COLOR)

                # B. Thời gian (Góc TRÊN PHẢI)
                now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                (tw, th), _ = cv2.getTextSize(now_str, cv2.FONT_HERSHEY_SIMPLEX, COMMON_FONT_SCALE, COMMON_THICKNESS)
                
                put_text_with_outline(resized, now_str, TARGET_WIDTH - tw - 20, 40, 
                                      COMMON_FONT_SCALE, COMMON_THICKNESS, TEXT_COLOR)
                
                # === 4. NÉN & STREAM ===
                success, encoded_img = cv2.imencode(".jpg", resized, encode_param)
                if success:
                    final_bytes = encoded_img.tobytes()
                    with self.lock:
                        self.jpeg_bytes = final_bytes
                        self.raw_frame_for_ai = resized
                
                # === 5. GỬI AI XỬ LÝ ===
                frame_cnt += 1
                if frame_cnt % 3 == 0:
                    try: self.ai_queue.put_nowait({'cam_id': self.cam_id, 'image': resized, 'scale': 1.0})
                    except: pass
            else:
                time.sleep(0.01)
            time.sleep(0.001)
        
        cap.release()

    def get_jpeg(self):
        with self.lock: return self.jpeg_bytes
    def get_snapshot(self):
        with self.lock:
            if self.raw_frame_for_ai is None: return None
            _, enc = cv2.imencode(".jpg", self.raw_frame_for_ai, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            return enc.tobytes()

# ... (Class CameraSystem giữ nguyên)
class CameraSystem:
    def __init__(self):
        self.cameras: Dict[int, CameraRuntime] = {}
        self.ai_input = multiprocessing.Queue(maxsize=3)
        self.ai_output = multiprocessing.Queue()
        self.system_stats = { "cpu": 0.0, "ram": 0.0, "threads": 0 }
        self.ai_process = multiprocessing.Process(target=run_ai_process, args=(self.ai_input, self.ai_output, "yolov8n.pt"), daemon=True)
        self.ai_process.start()
        self.is_system_running = True
        signal.signal(signal.SIGINT, self._signal_handler)
        threading.Thread(target=self._listen_ai, daemon=True).start()
        threading.Thread(target=self._monitor_resources, daemon=True).start()

    def _signal_handler(self, sig, frame):
        self.shutdown(); sys.exit(0)
    
    def _monitor_resources(self):
        p = psutil.Process()
        while self.is_system_running:
            try:
                self.system_stats = {"cpu": round(p.cpu_percent(),1), "ram": round(p.memory_info().rss/1048576,1), "threads": threading.active_count()}
                time.sleep(2)
            except: pass

    def _listen_ai(self):
        while self.is_system_running:
            try:
                r = self.ai_output.get(timeout=0.5)
                if r['cam_id'] in self.cameras: 
                    self.cameras[r['cam_id']].ai_metadata = r.get('data', [])
            except: pass

    def get_camera(self, cid): return self.cameras.get(cid)
    def add_camera(self, cid, src):
        if cid in self.cameras: self.cameras[cid].stop()
        self.cameras[cid] = CameraRuntime(cid, src, self.ai_input)
    def shutdown(self):
        self.is_system_running = False
        for c in self.cameras.values(): c.stop()
        if self.ai_process.is_alive(): self.ai_process.terminate()

camera_system = CameraSystem()