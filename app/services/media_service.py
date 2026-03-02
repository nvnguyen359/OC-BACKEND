# app/services/media_service.py
import os
import cv2
import time
import queue
import threading
import subprocess
from dotenv import load_dotenv

from app.db.session import SessionLocal
from app.db.models import Setting, Order
from app.services.order_repository import order_repo

# Load biến môi trường từ file .env
load_dotenv()

class LocalMediaService:
    def __init__(self):
        self.default_folder = "OC-media"
        self.post_process_queue = queue.Queue()
        
        # Luồng duy nhất: Nén Video (Chạy ngay sau khi chốt đơn và chỉ lưu cục bộ)
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

    def save_snapshot(self, frame, code: str, order_id: int = None) -> str:
        """Chỉ lưu ảnh cục bộ thật nhanh, trả về đường dẫn local"""
        try:
            root = self.get_storage_path()
            d = os.path.join(root, "avatars")
            os.makedirs(d, exist_ok=True)
            filename = f"{code}.jpg"
            full_path = os.path.join(d, filename)
            
            # Lưu ảnh ra máy ngay lập tức (Không upload ở đây)
            cv2.imwrite(full_path, frame)
            
            if order_id:
                order_repo.update_avatar(order_id, full_path)
            
            return full_path
                
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
        """Nén video xong chỉ lưu cục bộ"""
        while True:
            try:
                task = self.post_process_queue.get()
                if task is None: break
                
                src = task['src']
                order_id = task['order_id']
                
                if not os.path.exists(src):
                    continue

                root = self.get_storage_path()
                date_str = task['created_at'].strftime("%Y/%m/%d")
                final_dir = os.path.join(root, "videos", date_str)
                os.makedirs(final_dir, exist_ok=True)
                
                filename = f"{task['code']}_{int(task['created_at'].timestamp())}.mp4"
                dest = os.path.join(final_dir, filename)
                
                # Ép FFmpeg chạy 1 nhân, tối ưu phần cứng Orange Pi
                cmd = [
                    'ffmpeg', '-y', '-v', 'error', 
                    '-i', src,
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '30',
                    '-threads', '1', 
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    dest
                ]
                subprocess.run(cmd)
                
                # Kiểm tra nén thành công
                if os.path.exists(dest) and os.path.getsize(dest) > 1024:
                    print(f"✅ Đã nén thành công MP4: {filename} (Chờ Up Drive ban đêm)")
                    
                    # Xóa dọn dẹp file .avi gốc an toàn
                    try:
                        if os.path.exists(src):
                            os.remove(src)
                            print(f"🗑️ Đã dọn dẹp file gốc: {src}")
                    except Exception as del_err:
                        print(f"⚠️ Hệ điều hành khóa file, chưa thể xóa {src}: {del_err}")
                    
                    if order_id:
                        try:
                            with SessionLocal() as db:
                                order = db.query(Order).get(order_id)
                                if order:
                                    order.path_video = f"{root}/videos/{date_str}/{filename}"
                                    db.commit()
                        except Exception as db_err:
                            print(f"⚠️ DB Update Error: {db_err}")
                else:
                    # Nén thất bại cũng cố gắng dọn file .avi
                    try:
                        if os.path.exists(src): os.remove(src)
                    except: pass
                    print(f"❌ Video Convert FAILED: {filename}")

                # Hạ nhiệt CPU
                time.sleep(3.0)

            except Exception as e:
                print(f"❌ Convert Worker Error: {e}")
                time.sleep(1.0) 

# Singleton Instance
media_service = LocalMediaService()