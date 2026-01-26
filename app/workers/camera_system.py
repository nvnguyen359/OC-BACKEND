# app/workers/camera_system.py
import sys
import threading
import time
import multiprocessing
import signal
import psutil
import os
from typing import Dict

# --- IMPORTS ---
from app.workers.ai_detector import run_ai_process
from app.db.session import SessionLocal
from app.workers.camera_runtime import CameraRuntime

class CameraSystem:
    def __init__(self):
        self.cameras: Dict[int, CameraRuntime] = {}
        # Queue AI
        self.ai_input = multiprocessing.Queue(maxsize=10)
        self.ai_output = multiprocessing.Queue()
        
        # Thống kê tài nguyên hệ thống
        self.system_stats = {
            "cpu": 0.0, 
            "ram": 0.0, 
            "threads": 0,
            "disk_total": 0.0,
            "disk_used": 0.0,
            "disk_free": 0.0,
            "disk_percent": 0.0
        }
        
        # Start AI Process
        # Daemon=True để tự tắt khi app chính tắt
        self.ai_process = multiprocessing.Process(
            target=run_ai_process, args=(self.ai_input, self.ai_output, "yolov8n.pt"), daemon=True
        )
        self.ai_process.start()
        
        self.is_system_running = True 
        try: 
            # Bắt tín hiệu Ctrl+C để dừng sạch sẽ
            signal.signal(signal.SIGINT, lambda s, f: (self.shutdown(), sys.exit(0)))
        except ValueError: pass
        
        # Start background threads
        threading.Thread(target=self._listen_ai, daemon=True).start()
        threading.Thread(target=self._monitor_resources, daemon=True).start()

        # [QUAN TRỌNG] Tự động load camera từ DB và chạy ngầm ngay khi khởi tạo
        threading.Thread(target=self._startup_load_cameras, daemon=True).start()

    def _startup_load_cameras(self):
        """Load danh sách camera từ DB và khởi chạy background."""
        
        # [TỐI ƯU ORANGE PI] Đợi 5s để API Server và DB khởi động ổn định hoàn toàn
        # Tránh việc chiếm CPU ngay khi vừa boot
        time.sleep(5) 
        
        print("🔄 [System] Auto-loading cameras from Database...")
        
        db = SessionLocal()
        try:
            from app.crud.camera_crud import camera_crud

            all_cams = camera_crud.get_all(db)
            if not all_cams:
                print("⚠️ [System] Database chưa có camera nào.")
                return

            active_count = 0
            for cam in all_cams:
                try:
                    # 1. Chỉ chạy camera ACTIVE
                    status = getattr(cam, 'status', 'UNKNOWN')
                    if status != 'ACTIVE':
                        continue 
                    
                    # 2. Xác định Source
                    source = None
                    rtsp = getattr(cam, 'rtsp_url', None)
                    os_index = getattr(cam, 'os_index', None)
                    dev_path = getattr(cam, 'device_path', None)

                    if rtsp and isinstance(rtsp, str) and len(rtsp) > 5:
                        source = rtsp
                    elif os_index is not None:
                        source = int(os_index)
                    elif dev_path:
                        if str(dev_path).isdigit():
                            source = int(dev_path)
                        else:
                            source = dev_path
                    
                    if source is None: source = cam.id - 1

                    print(f"▶️ [System] Background Start: Cam ID={cam.id} | Source={source}")
                    self.add_camera(cam.id, source)
                    active_count += 1
                    
                    # [TỐI ƯU ORANGE PI] QUAN TRỌNG NHẤT:
                    # Ngủ 3 giây giữa mỗi lần bật camera.
                    # Giúp CPU có thời gian nghỉ, không bị spike 100% làm treo Web UI.
                    time.sleep(3.0) 
                    
                except Exception as e:
                    print(f"❌ [System] Failed to start Cam {cam.id}: {e}")
            
            print(f"✅ [System] Loaded {active_count} active cameras running in background.")

        except Exception as e:
            print(f"❌ [System] Load Error: {e}")
        finally:
            db.close()

    def _monitor_resources(self):
        p = psutil.Process()
        while self.is_system_running:
            try:
                # [UPDATE] Lấy thông tin ổ cứng (phân vùng gốc /)
                # Nếu chạy trên Windows, thay '/' bằng 'C:\\'
                disk_path = '/' if os.name != 'nt' else 'C:\\'
                disk = psutil.disk_usage(disk_path) 
                
                self.system_stats = {
                    "cpu": round(p.cpu_percent(), 1),
                    # RAM convert sang MB
                    "ram": round(p.memory_info().rss / 1048576, 1), 
                    "threads": threading.active_count(),
                    # Disk convert sang GB
                    "disk_total": round(disk.total / (1024**3), 1),
                    "disk_used": round(disk.used / (1024**3), 1),
                    "disk_free": round(disk.free / (1024**3), 1),
                    "disk_percent": disk.percent
                }
                # Check mỗi 2 giây
                time.sleep(2)
            except Exception as e:
                # print(f"⚠️ Stats Error: {e}")
                pass

    def _listen_ai(self):
        while self.is_system_running:
            try:
                # Timeout ngắn để check biến is_system_running thường xuyên
                r = self.ai_output.get(timeout=0.5)
                if r['cam_id'] in self.cameras:
                    self.cameras[r['cam_id']].ai_metadata = r.get('data', [])
            except: pass

    # =================================================================
    # Logic Thêm/Xóa Camera
    # =================================================================
    def add_camera(self, cid, src):
        if cid in self.cameras: 
            cam = self.cameras[cid]
            # [QUAN TRỌNG] Nếu đang chạy tốt -> Bỏ qua, KHÔNG báo lỗi, KHÔNG khởi động lại
            if cam.is_running and cam.is_connected:
                print(f"ℹ️ Camera {cid} is already running (Background). Keep alive.")
                return
            else:
                # Nếu tồn tại nhưng đã chết -> Dọn dẹp để khởi tạo lại
                print(f"⚠️ Camera {cid} stopped/zombie. Restarting...")
                self.stop_camera(cid)

        # Khởi tạo mới
        print(f"🚀 [System] Starting Camera {cid}...")
        self.cameras[cid] = CameraRuntime(cid, src, self.ai_input)
    
    def stop_camera(self, cid):
        """Hàm này dừng và XÓA khỏi bộ nhớ. Chỉ dùng khi Shutdown hoặc Delete hẳn."""
        if cid in self.cameras:
            try: self.cameras[cid].stop()
            except: pass
            del self.cameras[cid]

    def get_camera(self, cid): return self.cameras.get(cid)
    
    def shutdown(self):
        print("🔻 [System] Shutting down...")
        self.is_system_running = False
        # Dừng tất cả camera con
        for c in list(self.cameras.values()): c.stop()
        # Dừng tiến trình AI
        if self.ai_process.is_alive(): self.ai_process.terminate()

# Singleton Instance
camera_system = CameraSystem()