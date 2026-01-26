# app/workers/upsert_camera_worker.py
import os
import threading
import time
import platform
import sys

# 1. CẤU HÌNH TẮT LOG RÁC
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
    
    # [QUAN TRỌNG] Import khóa và class từ camera_stream
    # Class này đã được FIX (bỏ os.dup2) nên sẽ không gây lỗi PermissionError nữa
    from app.workers.camera_stream import FailsafeSuppressStderr, _global_cam_lock
except ImportError:
    SessionLocal = None; camera_crud = None; schemas = None; camera_system = None
    FailsafeSuppressStderr = None; _global_cam_lock = None

# ==============================================================================
# Helper: Ping thiết bị vật lý
# ==============================================================================
def check_physical_device(os_index: int) -> bool:
    if cv2 is None: return False
    is_opened = False
    cap = None
    try:
        backend = cv2.CAP_DSHOW if platform.system() == 'Windows' else cv2.CAP_V4L2
        
        # [FIX] Dùng _global_cam_lock để xếp hàng, tránh đánh nhau với CameraRuntime
        lock_acquired = False
        if _global_cam_lock:
            # Chờ tối đa 2s để lấy khóa
            lock_acquired = _global_cam_lock.acquire(timeout=2.0)
            
        try:
            # Chỉ mở cam nếu lấy được khóa hoặc đang test đơn lẻ
            if lock_acquired or (_global_cam_lock is None):
                if FailsafeSuppressStderr:
                    with FailsafeSuppressStderr():
                        cap = cv2.VideoCapture(os_index, backend)
                else:
                    cap = cv2.VideoCapture(os_index, backend)
                
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        is_opened = True
        finally:
            if cap: cap.release()
            if lock_acquired and _global_cam_lock:
                _global_cam_lock.release()
            
            # Ngủ ngắn để Windows giải phóng driver
            time.sleep(0.5)
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

                for idx in range(self.max_scan_index + 1):
                    is_alive = False
                    
                    if is_system_using_index(idx):
                        is_alive = True
                    else:
                        is_alive = check_physical_device(idx)

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
                                print(f"❌ [Disconnect] Camera {idx} unplugged (Status Only).")
                                self._update_db(db, cam, 'DISCONNECTED', 0)
                                # Không gọi lệnh STOP để tránh xung đột
                                # self._sync_system(cam.id, idx, 'STOP')

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