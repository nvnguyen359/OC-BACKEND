# app/workers/disk_manager_worker.py
import os
import time
import threading
import psutil
from datetime import datetime, date
from sqlalchemy import or_

# Imports DB
from app.db.session import SessionLocal
from app.db import models

class DiskManager:
    def __init__(self, check_hour=3, min_gb=2.0, target_gb=4.0):
        self.check_hour = check_hour   # 3h sáng
        self.min_free_bytes = min_gb * (1024**3)    # 2GB
        self.target_free_bytes = target_gb * (1024**3) # 4GB
        self.is_running = False
        self.thread = None
        self.last_run_date = None
        self.path_to_check = "/" 
        
        if os.name == 'nt': 
            self.path_to_check = os.getcwd()[:3] 

    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print(f"🧹 [DiskManager] Started. Schedule: Check every hour (Target: {self.check_hour}:00).")

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print("🧹 [DiskManager] Stopped.")

    def _monitor_loop(self):
        while self.is_running:
            # Ngủ 1 tiếng (3600s), check stop mỗi giây
            for _ in range(3600):
                if not self.is_running: return
                time.sleep(1)
            
            now = datetime.now()
            # Nếu đúng giờ và chưa chạy hôm nay
            if now.hour == self.check_hour:
                if self.last_run_date != now.date():
                    print(f"🕒 [DiskManager] It's {self.check_hour} AM. Checking disk space...")
                    self._check_and_clean()
                    self.last_run_date = now.date()

    def _get_free_space(self):
        try:
            usage = psutil.disk_usage(self.path_to_check)
            return usage.free
        except Exception:
            return 0

    def _check_and_clean(self):
        free_space = self._get_free_space()
        free_gb = free_space / (1024**3)
        print(f"💾 [DiskManager] Current Free: {free_gb:.2f} GB")

        if free_space < self.min_free_bytes:
            print(f"⚠️ [DiskManager] Disk Low (<2GB). Starting cleanup...")
            self._perform_cleanup()
        else:
            print("✅ [DiskManager] Disk space is healthy.")

    def _perform_cleanup(self):
        db = SessionLocal()
        try:
            deleted_count = 0
            while self._get_free_space() < self.target_free_bytes and self.is_running:
                # 1. Tìm đơn cũ nhất có file
                oldest_order = db.query(models.Order).filter(
                    or_(
                        models.Order.path_video.isnot(None),
                        models.Order.path_avatar.isnot(None)
                    )
                ).order_by(models.Order.created_at.asc()).first()

                if not oldest_order:
                    print("⚠️ [DiskManager] No more orders with files to delete.")
                    break

                # 2. Xóa file vật lý
                self._delete_file(oldest_order.path_video)
                self._delete_file(oldest_order.path_avatar)

                # 3. Xóa record DB
                print(f"🗑️ Deleting Order Record: {oldest_order.code} (ID: {oldest_order.id})")
                db.delete(oldest_order)
                db.commit()
                
                deleted_count += 1
                time.sleep(0.1)

            print(f"✅ [DiskManager] Cleanup Finished. Deleted {deleted_count} orders.")

        except Exception as e:
            print(f"❌ [DiskManager] Error: {e}")
            db.rollback()
        finally:
            db.close()

    def _delete_file(self, path):
        if path and os.path.exists(path):
            try: os.remove(path)
            except Exception: pass

# Singleton Instance
disk_manager_worker = DiskManager()