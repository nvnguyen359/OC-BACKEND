from app.workers.camera_worker import camera_worker
from app.workers.db_syncer import run_db_sync_worker

from app.workers.camera_worker import camera_worker
from app.workers.db_syncer import run_db_sync_worker

def start_all_workers():
    """
    Hàm duy nhất để bật toàn bộ hệ thống background.
    """
    print("============== STARTING WORKERS ==============")
    
    # 1. Bật AI và Camera Manager
    # [FIX] Dùng camera_worker
    camera_worker.start_system()

    # 2. Bật Thread đồng bộ DB (Nếu cần)
    run_db_sync_worker(interval=5)

    print("================ WORKERS READY ===============")

def stop_all_workers():
    print("============== STOPPING WORKERS ==============")
    # [FIX] Dùng camera_worker
    camera_worker.shutdown()