# app/workers/upsert_camera_worker.py
import os
import threading
import time
import platform
import sys
import traceback

# 1. CẤU HÌNH TẮT LOG RÁC CỦA OPENCV
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_OBSENSOR"] = "0"

try: 
    import cv2
except ImportError: 
    cv2 = None

try:
    from app.db.session import SessionLocal 
    from app.crud.camera_crud import camera_crud
    from app.db import schemas
    from app.workers.camera_worker import camera_system
    
    # Import khóa và class bổ trợ từ camera_stream
    from app.workers.camera_stream import FailsafeSuppressStderr, _global_cam_lock
except ImportError:
    SessionLocal = None; camera_crud = None; schemas = None; camera_system = None
    FailsafeSuppressStderr = None; _global_cam_lock = None

# ==============================================================================
# Helper: Kiểm tra thiết bị vật lý có phản hồi không
# ==============================================================================
def check_physical_device(os_index: int) -> bool:
    if cv2 is None: return False
    is_opened = False
    cap = None
    try:
        # Windows dùng DSHOW để tránh treo khi khởi tạo
        backend = cv2.CAP_DSHOW if platform.system() == 'Windows' else cv2.CAP_V4L2
        
        lock_acquired = False
        if _global_cam_lock:
            # Chờ tối đa 2s để lấy khóa, tránh xung đột với các thread stream đang chạy
            lock_acquired = _global_cam_lock.acquire(timeout=2.0)
            
        try:
            if lock_acquired or (_global_cam_lock is None):
                if FailsafeSuppressStderr:
                    with FailsafeSuppressStderr():
                        cap = cv2.VideoCapture(os_index, backend)
                else:
                    cap = cv2.VideoCapture(os_index, backend)
                
                if cap.isOpened():
                    # Đọc thử 1 frame để chắc chắn cam không bị "treo" driver
                    ret, _ = cap.read()
                    if ret:
                        is_opened = True
        finally:
            if cap: cap.release()
            if lock_acquired and _global_cam_lock:
                _global_cam_lock.release()
            
            # Nghỉ 0.5s để OS kịp giải phóng tài nguyên driver
            time.sleep(0.5)
    except: 
        pass
    return is_opened

# ==============================================================================
# Helper: Kiểm tra index đang được hệ thống sử dụng và thread còn sống không
# ==============================================================================
def is_system_using_index(idx: int) -> bool:
    if not camera_system: return False
    for cam_runner in camera_system.cameras.values():
        # [FIX] Chỉ coi là đang dùng nếu thread thực sự còn sống
        if getattr(cam_runner, 'is_running', False):
            try:
                src = None
                if hasattr(cam_runner, 'stream') and cam_runner.stream and hasattr(cam_runner.stream, 'source'):
                    src = cam_runner.stream.source
                
                if str(src) == str(idx): 
                    return True
            except Exception:
                continue
    return False

# ==============================================================================
# Worker Logic: Tự động phát hiện và đồng bộ Camera
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
        print(f"🛡️ [UpsertWorker] Auto-Discovery Started (Index 0-{self.max_scan_index})...")

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
                    db_cam = existing_cams.get(idx)
                    
                    # Nếu bị Admin tắt (OFF) thì không quét index này
                    if db_cam and db_cam.status == 'OFF':
                        continue

                    is_alive = False
                    is_running_in_system = is_system_using_index(idx)

                    # Ưu tiên kiểm tra trong system trước để tránh mở cam vật lý vô ích
                    if is_running_in_system:
                        is_alive = True
                    else:
                        is_alive = check_physical_device(idx)

                    if is_alive:
                        if db_cam:
                            # Tự động Re-connect nếu cam bị ngắt trước đó nhưng giờ đã có lại
                            if db_cam.status != 'ACTIVE' or not is_running_in_system:
                                if db_cam.status != 'OFF': 
                                    print(f"🔌 [Re-Connect] Camera {idx} detected. Starting...")
                                    self._update_db(db, db_cam, 'ACTIVE', 1)
                                    self._sync_system(db_cam.id, idx, 'START')
                        else:
                            print(f"🎉 [New Device] Found new Camera at Index {idx}. Adding to DB...")
                            new_cam = self._create_camera(db, idx)
                            if new_cam:
                                self._sync_system(new_cam.id, idx, 'START')
                    else:
                        # Nếu DB báo ACTIVE nhưng thực tế không thấy thiết bị -> Ngắt kết nối
                        if db_cam and db_cam.status == 'ACTIVE':
                            print(f"❌ [Disconnect] Camera {idx} unplugged.")
                            self._update_db(db, db_cam, 'DISCONNECTED', 0)
                            self._sync_system(db_cam.id, idx, 'STOP')

            except Exception as e: 
                print(f"⚠️ [Upsert Error] {e}")
            finally:
                if db: db.close()
            
            # Loop delay
            for _ in range(self.interval):
                if not self.is_running: break
                time.sleep(1)

    def _update_db(self, db, cam, status, is_connected):
        try:
            update_data = schemas.CameraUpdate(status=status, is_connected=is_connected)
            camera_crud.update(db, db_obj=cam, obj_in=update_data)
        except Exception as e:
            print(f"⚠️ [Update DB Error] Camera {cam.id}: {e}")

    def _create_camera(self, db, idx):
        try:
            # Khởi tạo đầy đủ thông tin để khớp với Pydantic Schema
            cam_in = {
                "name": f"Camera Local {idx}",
                "display_name": f"Camera Local {idx}",
                "unique_id": f"CAM_AUTO_{idx}_{int(time.time())}",
                "device_id": str(idx),
                "device_path": str(idx),
                "os_index": idx,
                "status": "ACTIVE",
                "is_connected": 1,
                "rtsp_url": ""
            }
            return camera_crud.upsert(db, cam_in)
        except Exception as e: 
            print(f"❌ [DB Insert Error] Lỗi khi tạo mới Camera {idx}: {e}")
            traceback.print_exc()
            return None

    def _sync_system(self, cam_id, idx, action):
        try:
            if action == 'START':
                # [FIX CRITICAL] Dùng camera_system.cameras.get() thay vì .get_camera()
                old_cam = camera_system.cameras.get(cam_id)
                if old_cam and not getattr(old_cam, 'is_running', False):
                    print(f"🧹 [Clean] Xóa luồng camera cũ đã chết: ID {cam_id}")
                    camera_system.stop_camera(cam_id)
                    time.sleep(0.5)

                # Kiểm tra trực tiếp trong dictionary .cameras
                if cam_id not in camera_system.cameras:
                    camera_system.add_camera(cam_id, idx)
            elif action == 'STOP':
                # Xóa hoàn toàn khỏi Dictionary để giải phóng tài nguyên
                camera_system.stop_camera(cam_id)
        except Exception as e:
            print(f"⚠️ [Sync System Error] {e}")

# Khởi tạo instance
upsert_camera_worker = UpsertCameraWorker(interval=5, max_scan_index=4)