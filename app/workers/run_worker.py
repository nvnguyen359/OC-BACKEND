# app/workers/run_worker.py
import time
# [QUAN TRỌNG] Import đúng 3 worker chính
from app.workers.camera_worker import camera_system
from app.workers.upsert_camera_worker import upsert_camera_worker
from app.workers.disk_manager_worker import disk_manager_worker

def start_all_workers():
    """
    Hàm khởi động toàn bộ hệ thống background.
    """
    print("============== STARTING WORKERS ==============")
    
    # 1. Kiểm tra Camera System (Đã tự chạy khi import singleton)
    if camera_system.is_system_running:
        print("✅ [RunWorker] Camera System is RUNNING.")
    else:
        print("⚠️ [RunWorker] Camera System is OFF.")

    # 2. Bật Upsert Worker (Quét DB thay đổi config)
    upsert_camera_worker.start()
    
    # 3. Bật Disk Manager Worker (Dọn dẹp ổ cứng lúc 3h sáng)
    disk_manager_worker.start()

    print("================ WORKERS STARTED =============")

    # Giữ main thread sống nếu file này được chạy trực tiếp (test)
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