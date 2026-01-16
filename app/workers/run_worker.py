# app/workers/run_worker.py
import time
# [QUAN TRỌNG] Import đúng 2 worker mới
from app.workers.camera_worker import camera_system
from app.workers.upsert_camera_worker import upsert_camera_worker

def start_all_workers():
    """
    Hàm khởi động toàn bộ hệ thống background.
    """
    print("============== STARTING WORKERS ==============")
    
    # 1. Kiểm tra Camera System (Đã tự chạy khi import)
    if camera_system.is_system_running:
        print("✅ [RunWorker] Camera System is RUNNING.")
    else:
        print("⚠️ [RunWorker] Camera System is OFF.")

    # 2. [FIX] Bật Upsert Worker (Thay thế db_syncer cũ)
    # Đây là worker thực hiện việc quét DB mỗi 5s
    upsert_camera_worker.start()

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
    camera_system.shutdown()
    print("================ WORKERS STOPPED =============")

if __name__ == "__main__":
    start_all_workers()