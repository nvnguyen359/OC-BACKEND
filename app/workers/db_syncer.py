import time
import threading
from app.db.session import get_db
from app.services.camera_service import CameraService
from app.db import schemas

def run_db_sync_worker(interval: int = 5):
    """
    WORKER THREAD: Định kỳ quét và update DB (giả lập upsert).
    """
    def _loop():
        print(f"🔄 [DB WORKER] Sync started (Interval: {interval}s)")
        while True:
            try:
                # Logic cũ của bạn: Upsert camera (Ví dụ giả lập)
                # Bạn có thể mở rộng logic quét IP thực tế ở đây
                pass 
            except Exception as e:
                print(f"⚠️ [DB WORKER] Error: {e}")
            time.sleep(interval)

    # Chạy thread daemon
    t = threading.Thread(target=_loop, daemon=True)
    t.start()