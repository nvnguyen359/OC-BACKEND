# app/services/upload_service.py
import os
import time
import threading
import pytz
from datetime import datetime
from dotenv import load_dotenv

from app.db.session import SessionLocal
from app.db.models import Order
from app.services.gdrive_service import gdrive_service
from app.crud.setting_crud import setting as setting_crud

# Load biến môi trường từ file .env
load_dotenv()

class UploadService:
    def __init__(self):
        # Khởi động Luồng săn việc kết hợp (Hybrid)
        threading.Thread(target=self._hybrid_upload_worker, daemon=True).start()

    def _hybrid_upload_worker(self):
        """Worker thông minh: Rảnh rỗi ban ngày up từ từ, ban đêm up tốc độ cao"""
        print("☁️ [System] Luồng Upload Thông Minh (Hybrid) đã khởi động...")
        
        # Đợi hệ thống khởi động xong hoàn toàn mới import camera_system để tránh Circular Import
        time.sleep(10)
        try:
            from app.workers.camera_system import camera_system
        except ImportError:
            camera_system = None

        while True:
            time.sleep(10) # Rút ngắn thời gian kiểm tra xuống 10s để phản ứng nhanh lúc rảnh
            try:
                db = SessionLocal()
                
                # 1. Kiểm tra tính năng GDrive
                storage_type = setting_crud.get_value(db, "storage_type")
                if storage_type != "gdrive":
                    db.close()
                    time.sleep(50)
                    continue
                    
                # 2. Đọc thư mục đích từ .env
                folder_id = os.getenv("TARGET_FOLDER_ID")
                if not folder_id:
                    db.close()
                    time.sleep(50)
                    continue
                
                default_folder = os.getenv("DEFAULT_FOLDER", "OC-media")
                
                # 3. Kiểm tra giờ kết thúc ca
                work_end_str = setting_crud.get_value(db, "work_end_time") or "18:30"
                try:
                    end_h, end_m = map(int, work_end_str.split(":"))
                except:
                    end_h, end_m = 18, 30
                    
                tz = pytz.timezone('Asia/Ho_Chi_Minh')
                now = datetime.now(tz)
                
                is_after_hours = False
                if now.hour > end_h or (now.hour == end_h and now.minute >= end_m) or now.hour < 6:
                    is_after_hours = True
                    
                # 4. Kiểm tra độ "Rảnh" của Camera (Điều kiện: Đã qua 5 phút không quét mã)
                is_idle = True
                if camera_system and hasattr(camera_system, 'cameras'):
                    current_time = time.time()
                    for cid, cam in camera_system.cameras.items():
                        # Đang có đơn được đóng -> Chắc chắn đang bận
                        if getattr(cam, 'recording', False):
                            is_idle = False
                            break
                        # Vừa quét mã trong 5 phút qua (300 giây) -> Coi như kho đang nhộn nhịp
                        last_scan = getattr(cam, 'last_scanned_time', 0)
                        if (current_time - last_scan) < 300:
                            is_idle = False
                            break
                        
                # 5. Quyết định làm việc
                if not is_after_hours and not is_idle:
                    db.close()
                    continue # Đang bận và vẫn trong giờ làm -> Tàng hình bỏ qua
                    
                # 6. Lấy danh sách file (Rảnh: 1 đơn/lần | Đêm: 10 đơn/lần). Ưu tiên up đơn cũ nhất trước (asc)
                fetch_limit = 10 if is_after_hours else 1
                orders = db.query(Order).filter(
                    (Order.path_avatar.like(f'%{default_folder}%')) | 
                    (Order.path_video.like(f'%{default_folder}%'))
                ).order_by(Order.id.asc()).limit(fetch_limit).all() 
                
                if not orders:
                    db.close()
                    time.sleep(60) # Kho đã đồng bộ xong xuôi -> Nghỉ 1 phút
                    continue

                if is_after_hours:
                    print(f"🌙 Đã hết ca làm việc. Chạy OverDrive tải lên {len(orders)} đơn hàng...")
                else:
                    print(f"☕ Kho đang rảnh rỗi. Tranh thủ đồng bộ {len(orders)} đơn hàng...")

                for order in orders:
                    # Xử lý tải Video
                    if order.path_video and default_folder in order.path_video:
                        if os.path.exists(order.path_video):
                            drive_link = gdrive_service.upload_file_and_get_link(order.path_video, folder_id, 'video/mp4')
                            if drive_link:
                                local_path = order.path_video
                                order.path_video = drive_link
                                db.commit()
                                try: os.remove(local_path)
                                except: pass
                        else:
                            order.path_video = None
                            db.commit()
                            
                    # Xử lý tải Avatar
                    if order.path_avatar and default_folder in order.path_avatar:
                        if os.path.exists(order.path_avatar):
                            drive_link = gdrive_service.upload_file_and_get_link(order.path_avatar, folder_id, 'image/jpeg')
                            if drive_link:
                                local_path = order.path_avatar
                                order.path_avatar = drive_link
                                db.commit()
                                try: os.remove(local_path) 
                                except: pass
                        else:
                            order.path_avatar = None
                            db.commit()
                            
                    # Khoảng trễ an toàn: Rảnh ban ngày thì chờ 5s để dưỡng sức CPU/Mạng. Đêm thì quất liên tục (1s).
                    time.sleep(1 if is_after_hours else 5)
                
                db.close()
            except Exception as e:
                print(f"❌ Hybrid Uploader Error: {e}")
                time.sleep(30)

# Singleton Instance kích hoạt khi được import
upload_service = UploadService()