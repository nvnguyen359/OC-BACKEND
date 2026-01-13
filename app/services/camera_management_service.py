# app/services/camera_management_service.py
import time
import platform
import sys
import os
from typing import List, Any
from sqlalchemy.orm import Session

# --- IMPORTS ---
from app.crud.camera_crud import camera_crud 
from app.db import schemas # Import module schemas để dùng CameraUpdate
from app.db.schemas import CameraOut as CameraResponse
from app.workers.camera_worker import camera_system

# Thư viện OpenCV
try:
    from cv2 import VideoCapture, CAP_DSHOW
except ImportError:
    VideoCapture = None 
    CAP_DSHOW = None

# ----------------------------------------------------------------------
# Helper: Kiểm tra kết nối vật lý của 1 Camera
# ----------------------------------------------------------------------
def check_camera_alive(os_index: int) -> bool:
    """
    Thử mở camera tại index chỉ định để xem nó có phản hồi không.
    """
    if VideoCapture is None:
        return False

    is_alive = False
    try:
        # Windows thường cần CAP_DSHOW để mở nhanh
        if platform.system() == 'Windows':
            cap = VideoCapture(os_index, CAP_DSHOW)
        else:
            cap = VideoCapture(os_index)
            
        if cap.isOpened():
            is_alive = True
            cap.release()
    except Exception:
        pass
    
    return is_alive

# ----------------------------------------------------------------------
# Camera Management Service (Health Check Logic)
# ----------------------------------------------------------------------

class CameraManagementService:
    def __init__(self, db: Session):
        self.db = db
        self.camera_crud = camera_crud 

    def sync_camera_status(self) -> List[CameraResponse]:
        """
        Duyệt qua danh sách Camera TRONG DB.
        Kiểm tra trạng thái thực tế và cập nhật lại DB + Worker.
        """
        # 1. Lấy tất cả camera đã lưu trong DB
        db_cameras = self.camera_crud.get_all(self.db)
        updated_list = []

        for cam in db_cameras:
            # Lấy index hệ điều hành (0, 1, 2...)
            current_os_index = cam.os_index
            if current_os_index is None and str(cam.device_path).isdigit():
                current_os_index = int(cam.device_path)
            
            if current_os_index is None:
                continue

            # 2. Kiểm tra trạng thái thực tế
            worker_cam = camera_system.get_camera(cam.id)
            is_physically_connected = False
            
            if worker_cam and worker_cam.is_running:
                is_physically_connected = True
            else:
                is_physically_connected = check_camera_alive(current_os_index)

            # 3. Cập nhật trạng thái vào DB nếu có thay đổi
            new_status = 'ACTIVE' if is_physically_connected else 'DISCONNECTED'
            new_is_connected = 1 if is_physically_connected else 0

            if cam.status != new_status or cam.is_connected != new_is_connected:
                print(f"🔄 State Change [ID {cam.id}]: {cam.status} -> {new_status}")
                
                # [FIX]: Dùng Pydantic Schema thay vì dict
                update_data = schemas.CameraUpdate(
                    status=new_status, 
                    is_connected=new_is_connected
                )
                
                # Update vào DB
                updated_cam = self.camera_crud.update(self.db, db_obj=cam, obj_in=update_data)
                updated_list.append(CameraResponse.model_validate(updated_cam))
            else:
                updated_list.append(CameraResponse.model_validate(cam))

            # 4. Đồng bộ Worker (Auto-start / Auto-stop)
            if new_status == 'ACTIVE':
                if not worker_cam:
                    print(f"🚀 Starting Worker for Camera ID {cam.id} (Index {current_os_index})")
                    try:
                        camera_system.add_camera(cam.id, current_os_index)
                    except Exception as e:
                        print(f"❌ Failed to start worker {cam.id}: {e}")
            else:
                if worker_cam:
                    print(f"🛑 Stopping Worker for Camera ID {cam.id} (Lost Connection)")
                    worker_cam.stop()

        return updated_list

# ----------------------------------------------------------------------
# Vòng lặp chạy ngầm
# ----------------------------------------------------------------------

def run_camera_upsert_loop(session_factory: Any, interval_seconds: int = 5):
    print(f"🛡️ Camera Health Check Service started (Interval: {interval_seconds}s)")
    
    while True:
        db = None
        try:
            db = session_factory()
            service = CameraManagementService(db)
            service.sync_camera_status()

        except Exception as e:
            print(f"❌ Error in Camera Health Check: {e}")
        finally:
            if db:
                db.close()
        
        time.sleep(interval_seconds)