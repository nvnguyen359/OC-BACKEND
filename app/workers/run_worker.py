# app/workers/run_worker.py
import time
from app.workers.camera_worker import camera_system
from app.workers.upsert_camera_worker import upsert_camera_worker
from app.workers.disk_manager_worker import disk_manager_worker

def start_all_workers():
    """
    Hàm khởi động toàn bộ hệ thống background.
    """
    print("============== STARTING WORKERS ==============")
    
    # 1. Kích hoạt Camera System (Lúc này mới thực sự chạy Process)
    camera_system.start()
    
    if camera_system.is_system_running:
        print("✅ [RunWorker] Camera System is RUNNING.")

    # 2. Bật Upsert Worker
    upsert_camera_worker.start()
    
    # 3. Bật Disk Manager Worker
    disk_manager_worker.start()

    print("================ WORKERS STARTED =============")

    if __name__ == "__main__":
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            stop_all_workers()

def stop_all_workers():
    print("\n============== STOPPING WORKERS ==============")
    upsert_camera_worker.stop()
    disk_manager_worker.stop()
    camera_system.shutdown()
    print("================ WORKERS STOPPED =============")

if __name__ == "__main__":
    start_all_workers()