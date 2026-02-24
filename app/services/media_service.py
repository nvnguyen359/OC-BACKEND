# app/services/media_service.py
import os
import cv2
import time
import queue
import threading
import subprocess
from datetime import datetime
from app.db.session import SessionLocal
from app.db.models import Setting, Order

# [NÂNG CẤP] Import service Google Drive và Order Repository
from app.services.gdrive_service import gdrive_service
from app.services.order_repository import order_repo

class LocalMediaService:
    def __init__(self):
        self.default_folder = "OC-media"
        self.post_process_queue = queue.Queue()
        threading.Thread(target=self._video_converter_worker, daemon=True).start()

    def get_storage_path(self) -> str:
        path = self.default_folder
        try:
            with SessionLocal() as db:
                setting = db.query(Setting).filter(Setting.key == "save_media").first()
                if setting and setting.value and setting.value.strip():
                    path = setting.value.strip()
        except: pass
        
        if not os.path.exists(path):
            try: os.makedirs(path, exist_ok=True)
            except: pass
        return path

    def create_video_writer(self, code: str, width: int, height: int, fps: float):
        root = self.get_storage_path()
        temp_dir = os.path.join(root, "temp_rec")
        os.makedirs(temp_dir, exist_ok=True)
        
        filepath = os.path.join(temp_dir, f"{code}_{int(time.time())}.avi")
        writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
        return writer, filepath

    # [NÂNG CẤP] Thêm order_id để tự động update DB khi có link Drive
    def save_snapshot(self, frame, code: str, order_id: int = None) -> str:
        try:
            root = self.get_storage_path()
            d = os.path.join(root, "avatars")
            os.makedirs(d, exist_ok=True)
            filename = f"{code}.jpg"
            full_path = os.path.join(d, filename)
            
            # Lưu ảnh tạm ra máy
            cv2.imwrite(full_path, frame)
            
            # [NÂNG CẤP] Đẩy lên Google Drive
            drive_link = gdrive_service.upload_file_and_get_link(full_path, mime_type='image/jpeg')
            
            if drive_link:
                if order_id:
                    order_repo.update_avatar(order_id, drive_link)
                # Tối ưu: Xóa ảnh ở Pi để tiết kiệm bộ nhớ sau khi lên cloud thành công
                if os.path.exists(full_path):
                    os.remove(full_path) 
                return drive_link
            else:
                # Fallback: Trả về link cục bộ nếu upload Drive thất bại
                return f"{root}/avatars/{filename}"
                
        except Exception as e:
            print(f"❌ Snapshot Error: {e}")
            return None

    def queue_video_conversion(self, src_path, code, created_at, order_db_id):
        if src_path and os.path.exists(src_path):
            self.post_process_queue.put({
                'src': src_path, 'code': code,
                'created_at': created_at, 'order_id': order_db_id
            })

    def _video_converter_worker(self):
        while True:
            try:
                task = self.post_process_queue.get()
                if task is None: break
                
                src = task['src']
                order_id = task['order_id']
                
                # Kiểm tra lại file gốc có tồn tại không
                if not os.path.exists(src):
                    continue

                root = self.get_storage_path()
                date_str = task['created_at'].strftime("%Y/%m/%d")
                final_dir = os.path.join(root, "videos", date_str)
                os.makedirs(final_dir, exist_ok=True)
                
                filename = f"{task['code']}_{int(task['created_at'].timestamp())}.mp4"
                dest = os.path.join(final_dir, filename)
                
                # [BẢO VỆ PHẦN CỨNG]: Ép FFmpeg chạy 1 nhân, giảm chất lượng nhẹ
                cmd = [
                    'ffmpeg', '-y', '-v', 'error', # Chỉ hiện log lỗi để đỡ rác console
                    '-i', src,
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '30',
                    '-threads', '1', 
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    dest
                ]
                subprocess.run(cmd)
                
                if os.path.exists(dest) and os.path.getsize(dest) > 1024: # Lớn hơn 1KB mới là file chuẩn
                    if os.path.exists(src): os.remove(src) # Xóa file tạm (.avi)
                    print(f"✅ Video Converted locally: {filename}")
                    
                    # [NÂNG CẤP] Đẩy video MP4 lên Google Drive
                    drive_link = gdrive_service.upload_file_and_get_link(dest, mime_type='video/mp4')
                    
                    if order_id:
                        try:
                            with SessionLocal() as db:
                                order = db.query(Order).get(order_id)
                                if order:
                                    # Nếu có drive_link thì dùng, không thì lưu đường dẫn local (Fallback)
                                    if drive_link:
                                        order.path_video = drive_link
                                    else:
                                        order.path_video = f"{root}/videos/{date_str}/{filename}"
                                    
                                    db.commit()
                                    if drive_link:
                                        print(f"✅ Đã lưu link Drive vào Database cho đơn {task['code']}")
                                    
                        except Exception as db_err:
                            print(f"⚠️ DB Update Error: {db_err}")
                            
                    # Nếu upload Drive thành công, xóa file MP4 ở máy đi cho nhẹ
                    if drive_link and os.path.exists(dest):
                        os.remove(dest)
                        print(f"🗑️ Đã xóa video cục bộ {filename} để tiết kiệm dung lượng.")
                        
                else:
                    # Nếu convert lỗi, cố gắng xóa file tạm để chống đầy ổ cứng
                    print(f"❌ Video Convert FAILED: {filename}")
                    if os.path.exists(src): os.remove(src)

                # [HẠ NHIỆT CPU]: Nghỉ 3 giây trước khi nén video tiếp theo
                time.sleep(3.0)

            except Exception as e:
                print(f"❌ Convert Worker Error: {e}")
                time.sleep(1.0) # Tránh crash vòng lặp vô hạn

# Singleton Instance
media_service = LocalMediaService()