# app/workers/camera_worker.py
import os

# ==============================================================================
# [QUAN TRỌNG] CẤU HÌNH TẮT LOG OPENCV (Phải đặt trước khi import cv2)
# ==============================================================================
os.environ["OPENCV_LOG_LEVEL"] = "OFF"           # Tắt log OpenCV
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"         # Tắt debug VideoIO
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0" # Tắt ưu tiên MSMF nếu cần (hoặc bỏ dòng này nếu muốn dùng mặc định)
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"

import threading
import time
import cv2  # <--- Import cv2 phải nằm SAU các lệnh os.environ
import multiprocessing
import queue
import platform
import signal
import psutil
from typing import Dict, Optional, Any
from app.workers.ai_detector import run_ai_process

# Chúng ta chỉ cố định Chiều ngang (Width) để đảm bảo băng thông
TARGET_WIDTH = 1280 

class CameraRuntime:
    def __init__(self, cam_id: int, source: Any, ai_queue: multiprocessing.Queue):
        self.cam_id = cam_id
        self.source = source
        self.ai_queue = ai_queue
        
        self.is_running = False
        self.thread = None
        self.processed_frame = None
        self.lock = threading.Lock()
        
        self.ai_metadata = [] 
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
            self.processed_frame = None

    def _capture_loop(self):
        src = self.source
        if isinstance(src, str):
            if src.startswith("Index_"):
                try: src = int(src.replace("Index_", ""))
                except: pass
            elif src.isdigit():
                src = int(src)
            
        print(f"📷 [Worker] Starting Camera {self.cam_id} (Source: {src})")

        if isinstance(src, int) and platform.system() == 'Windows':
            cap = cv2.VideoCapture(src, cv2.CAP_ANY)
            try:
                fourcc = cv2.VideoWriter.fourcc(*'MJPG')
            except:
                # Fallback nếu hàm trên lỗi: Tính toán thủ công mã FourCC cho MJPG
                fourcc = ord('M') | (ord('J') << 8) | (ord('P') << 16) | (ord('G') << 24)

            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) 
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            # cap.set(cv2.CAP_PROP_AUTOFOCUS, 1) # Có thể bỏ nếu gây lỗi focus
        else:
            cap = cv2.VideoCapture(src)
            
        if not cap.isOpened():
            print(f"❌ [Worker] Failed to open Camera {self.cam_id}")
            self.is_running = False
            return
        
        real_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        real_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        # Tính toán resize
        scale_factor = TARGET_WIDTH / real_w if real_w > 0 else 1.0
        final_w = TARGET_WIDTH
        final_h = int(real_h * scale_factor) if real_h > 0 else 720
        
        print(f"✅ [Worker] Cam {self.cam_id}: {int(real_w)}x{int(real_h)} -> Resize to {final_w}x{final_h}")

        frame_count = 0
        while self.is_running:
            ret, raw_frame = cap.read()
            if ret:
                resized = cv2.resize(raw_frame, (final_w, final_h), interpolation=cv2.INTER_AREA)

                with self.lock:
                    self.processed_frame = resized
                
                frame_count += 1
                if frame_count % 3 == 0:
                    try:
                        if not self.ai_queue.full():
                            self.ai_queue.put_nowait({
                                'cam_id': self.cam_id,
                                'image': resized.copy(), 
                                'scale': 1.0 
                            })
                    except queue.Full:
                        pass
            else:
                time.sleep(0.1) 
            time.sleep(0.005)
        
        cap.release()
        print(f"🛑 [Worker] Camera {self.cam_id} stopped.")

    def get_jpeg(self) -> Optional[bytes]:
        with self.lock:
            if self.processed_frame is None: return None
            success, encoded = cv2.imencode(".jpg", self.processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            return encoded.tobytes() if success else None

    def get_snapshot(self) -> Optional[bytes]:
        with self.lock:
            if self.processed_frame is None: return None
            success, encoded = cv2.imencode(".jpg", self.processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            return encoded.tobytes() if success else None
    
    def start_recording(self, order_code: str):
        self.recording = True
        self.order_code = order_code

    def stop_recording(self):
        self.recording = False
        self.order_code = None

class CameraSystem:
    def __init__(self):
        self.cameras: Dict[int, CameraRuntime] = {}
        self.ai_input = multiprocessing.Queue(maxsize=3)
        self.ai_output = multiprocessing.Queue()
        self.system_stats = { "cpu": 0.0, "ram": 0.0, "threads": 0 }
        
        self.ai_process = multiprocessing.Process(
            target=run_ai_process,
            args=(self.ai_input, self.ai_output, "yolov8n.pt"),
            daemon=True
        )
        self.ai_process.start()
        
        self.is_system_running = True
        threading.Thread(target=self._listen_ai, daemon=True).start()
        threading.Thread(target=self._monitor_resources, daemon=True).start()

    def _monitor_resources(self):
        try:
            process = psutil.Process(os.getpid())
            print("📊 [System] Resource Monitor Started...")
            while self.is_system_running:
                try:
                    cpu = process.cpu_percent(interval=None)
                    mem = process.memory_info()
                    ram_mb = mem.rss / (1024 * 1024)
                    self.system_stats = {
                        "cpu": round(cpu, 1),
                        "ram": round(ram_mb, 1),
                        "threads": threading.active_count()
                    }
                    time.sleep(2)
                except Exception: time.sleep(2)
        except ImportError: pass

    def _listen_ai(self):
        while self.is_system_running:
            try:
                res = self.ai_output.get(timeout=0.5)
                cam_id = res.get('cam_id')
                if cam_id in self.cameras:
                    # Logic update & reset
                    self.cameras[cam_id].ai_metadata = res.get('data', [])
            except: 
                pass

    def get_camera(self, cam_id: int) -> Optional[CameraRuntime]:
        return self.cameras.get(cam_id)

    def add_camera(self, cam_id: int, source: Any):
        if cam_id in self.cameras: 
            self.cameras[cam_id].stop()
        self.cameras[cam_id] = CameraRuntime(cam_id, source, self.ai_input)

    def shutdown(self):
        print("🛑 [System] Shutting down...")
        self.is_system_running = False
        for c in self.cameras.values(): c.stop()
        self.cameras.clear()
        if self.ai_process.is_alive():
            self.ai_process.terminate()
            try: os.kill(self.ai_process.pid, signal.SIGKILL)
            except: pass
        print("✅ [System] Stopped.")

camera_system = CameraSystem()