# app/workers/upsert_camera_worker.py
import os
import threading
import time
import platform
import sys

# 1. CẤU HÌNH TẮT LOG RÁC (Vẫn giữ)
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_OBSENSOR"] = "0"

try: import cv2
except ImportError: cv2 = None

try:
    from app.db.session import SessionLocal 
    from app.crud.camera_crud import camera_crud
    from app.db import schemas
    from app.workers.camera_worker import camera_system 
except ImportError:
    SessionLocal = None; camera_crud = None; schemas = None; camera_system = None

# ==============================================================================
# [MỚI] CLASS CHẶN LOG C++ (STDERR)
# ==============================================================================
class FailsafeSuppressStderr:
    """
    Context Manager để chuyển hướng stderr sang devnull tạm thời.
    Giúp chặn các log Warning từ tầng C++ của OpenCV.
    """
    def __enter__(self):
        self.active = False
        try:
            # Flush để đảm bảo log cũ đã in hết
            sys.stderr.flush()
            # Lưu file descriptor hiện tại của stderr
            self.err_fd = sys.stderr.fileno()
            self.saved_err_fd = os.dup(self.err_fd)
            # Mở null device
            self.devnull = os.open(os.devnull, os.O_RDWR)
            # Gán stderr vào null device
            os.dup2(self.devnull, self.err_fd)
            self.active = True
        except Exception:
            # Nếu môi trường không hỗ trợ fileno (VD: một số IDE console), bỏ qua
            pass

    def __exit__(self, exc_type, exc_value, traceback):
        if self.active:
            try:
                sys.stderr.flush()
                # Khôi phục stderr cũ
                os.dup2(self.saved_err_fd, self.err_fd)
                os.close(self.saved_err_fd)
                os.close(self.devnull)
            except Exception:
                pass

# ==============================================================================
# Helper: Ping thiết bị vật lý
# ==============================================================================
def check_physical_device(os_index: int) -> bool:
    if cv2 is None: return False
    is_opened = False
    try:
        # Windows dùng CAP_DSHOW hoặc CAP_ANY
        backend = cv2.CAP_DSHOW if platform.system() == 'Windows' else cv2.CAP_V4L2
        
        # [ÁP DỤNG TẠI ĐÂY] Bọc hàm mở camera trong SuppressStderr
        with FailsafeSuppressStderr():
            cap = cv2.VideoCapture(os_index, backend)
        
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                is_opened = True
            cap.release()
    except: 
        pass
    return is_opened

# ==============================================================================
# Helper: Kiểm tra System
# ==============================================================================
def is_system_using_index(idx: int) -> bool:
    if not camera_system: return False
    for cam_runner in camera_system.cameras.values():
        if cam_runner.is_running:
            src = cam_runner.source
            if str(src) == str(idx): 
                return True
    return False

# ==============================================================================
# Worker Logic
# ==============================================================================
class UpsertCameraWorker:
    def __init__(self, interval=5, max_scan_index=4):
        self.interval = interval
        self.max_scan_index = max_scan_index
        self.is_running = False
        self.thread = None

    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"🛡️ [UpsertWorker] Auto-Discovery Started (Scan Index 0-{self.max_scan_index})...")

    def stop(self):
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        print("🛡️ [UpsertWorker] Stopped.")

    def _run_loop(self):
        while self.is_running:
            if not SessionLocal or not camera_crud:
                time.sleep(self.interval)
                continue

            db = None
            try:
                db = SessionLocal()
                existing_cams = {}
                db_cameras = camera_crud.get_all(db)
                for cam in db_cameras:
                    idx = cam.os_index
                    if idx is None and str(cam.device_path).isdigit():
                        idx = int(cam.device_path)
                    if idx is not None:
                        existing_cams[idx] = cam

                # Quét Index
                for idx in range(self.max_scan_index + 1):
                    is_alive = False
                    
                    # 1. Check System (Ưu tiên)
                    if is_system_using_index(idx):
                        is_alive = True
                    else:
                        # 2. Check Vật lý (Đã bọc chống log)
                        is_alive = check_physical_device(idx)

                    # Logic Upsert
                    if is_alive:
                        if idx in existing_cams:
                            cam = existing_cams[idx]
                            if cam.status != 'ACTIVE':
                                print(f"🔌 [Re-Connect] Camera {idx} is back online.")
                                self._update_db(db, cam, 'ACTIVE', 1)
                                self._sync_system(cam.id, idx, 'START')
                        else:
                            print(f"🎉 [New Device] Found new Camera at Index {idx}. Adding to DB...")
                            new_cam = self._create_camera(db, idx)
                            if new_cam:
                                self._sync_system(new_cam.id, idx, 'START')
                    else:
                        if idx in existing_cams:
                            cam = existing_cams[idx]
                            if cam.status == 'ACTIVE':
                                print(f"❌ [Disconnect] Camera {idx} unplugged.")
                                self._update_db(db, cam, 'DISCONNECTED', 0)
                                self._sync_system(cam.id, idx, 'STOP')

            except Exception: pass
            finally:
                if db: db.close()
            
            for _ in range(self.interval):
                if not self.is_running: break
                time.sleep(1)

    def _update_db(self, db, cam, status, is_connected):
        try:
            update_data = schemas.CameraUpdate(status=status, is_connected=is_connected)
            camera_crud.update(db, db_obj=cam, obj_in=update_data)
        except: pass

    def _create_camera(self, db, idx):
        try:
            cam_in = {
                "name": f"Camera {idx}",
                "unique_id": f"CAM_AUTO_{idx}_{int(time.time())}",
                "device_id": str(idx),
                "device_path": str(idx),
                "os_index": idx,
                "status": "ACTIVE",
                "is_connected": 1,
                "rtsp_url": ""
            }
            return camera_crud.upsert(db, cam_in)
        except Exception: return None

    def _sync_system(self, cam_id, idx, action):
        try:
            if action == 'START':
                if not camera_system.get_camera(cam_id):
                    camera_system.add_camera(cam_id, idx)
            elif action == 'STOP':
                if camera_system.get_camera(cam_id):
                    camera_system.get_camera(cam_id).stop()
        except: pass

upsert_camera_worker = UpsertCameraWorker(interval=5, max_scan_index=4)