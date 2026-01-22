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

class LocalMediaService:
    def __init__(self):
        self.default_folder = "OC-media"
        self.post_process_queue = queue.Queue()
        # Khởi chạy luồng xử lý video ngầm
        threading.Thread(target=self._video_converter_worker, daemon=True).start()

    def get_storage_path(self) -> str:
        """
        Lấy tên folder gốc từ DB (Ví dụ: 'OC-media').
        Nếu chưa có folder thì tự tạo.
        """
        path = self.default_folder
        try:
            db = SessionLocal()
            setting = db.query(Setting).filter(Setting.key == "save_media").first()
            if setting and setting.value and setting.value.strip():
                path = setting.value.strip()
            db.close()
        except: pass
        
        # Tạo folder vật lý nếu chưa có
        if not os.path.exists(path):
            try: os.makedirs(path, exist_ok=True)
            except: pass
            
        return path

    def create_video_writer(self, code: str, width: int, height: int, fps: float):
        """
        Tạo đối tượng ghi hình.
        Trả về (writer, đường_dẫn_file_tạm)
        """
        root = self.get_storage_path()
        temp_dir = os.path.join(root, "temp_rec")
        os.makedirs(temp_dir, exist_ok=True)
        
        filepath = os.path.join(temp_dir, f"{code}_{int(time.time())}.avi")
        
        # MJPG cho nhẹ máy, convert sau
        writer = cv2.VideoWriter(
            filepath, 
            cv2.VideoWriter_fourcc(*'MJPG'), 
            fps, 
            (width, height)
        )
        return writer, filepath

    def save_snapshot(self, frame, code: str) -> str:
        """
        Lưu ảnh Avatar và trả về đường dẫn ĐẦY ĐỦ (bao gồm folder gốc).
        Ví dụ: 'OC-media/avatars/CODE.jpg'
        """
        try:
            root = self.get_storage_path() # Lấy 'OC-media'
            
            # Tạo folder avatars bên trong root
            d = os.path.join(root, "avatars")
            os.makedirs(d, exist_ok=True)
            
            filename = f"{code}.jpg"
            full_path = os.path.join(d, filename)
            
            # Ghi file
            cv2.imwrite(full_path, frame)
            
            # [FIX] Trả về đường dẫn có kèm Root để khớp với URL Mount
            # Kết quả: "OC-media/avatars/CODE.jpg"
            # Lưu ý: Dùng dấu gạch chéo '/' chuẩn Web thay vì os.path.join (có thể ra '\' trên Win)
            return f"{root}/avatars/{filename}"
            
        except Exception as e:
            print(f"❌ Snapshot Error: {e}")
            return None

    def queue_video_conversion(self, src_path, code, created_at, order_db_id):
        """Đẩy task convert vào hàng đợi"""
        if src_path and os.path.exists(src_path):
            self.post_process_queue.put({
                'src': src_path,
                'code': code,
                'created_at': created_at,
                'order_id': order_db_id
            })

    def _video_converter_worker(self):
        """Luồng chạy ngầm xử lý FFmpeg"""
        while True:
            try:
                task = self.post_process_queue.get()
                if task is None: break
                
                src = task['src']
                order_id = task['order_id']
                
                # Lấy root dynamic (đề phòng user đổi setting lúc runtime)
                root = self.get_storage_path()
                
                date_str = task['created_at'].strftime("%Y/%m/%d")
                final_dir = os.path.join(root, "videos", date_str)
                os.makedirs(final_dir, exist_ok=True)
                
                filename = f"{task['code']}_{int(task['created_at'].timestamp())}.mp4"
                dest = os.path.join(final_dir, filename)
                
                # Lệnh FFmpeg tối ưu
                cmd = [
                    'ffmpeg', '-y', '-v', 'quiet',
                    '-i', src,
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    dest
                ]
                subprocess.run(cmd)
                
                if os.path.exists(dest):
                    if os.path.exists(src): os.remove(src)
                    
                    # Update DB
                    if order_id:
                        db = SessionLocal()
                        order = db.query(Order).get(order_id)
                        if order:
                            # [FIX] Lưu đường dẫn video kèm Root Folder
                            # Kết quả: "OC-media/videos/2023/10/05/CODE_123456.mp4"
                            order.path_video = f"{root}/videos/{date_str}/{filename}"
                            db.commit()
                        db.close()
                    print(f"✅ Video Converted: {filename}")
            except Exception as e:
                print(f"❌ Convert Error: {e}")

# Singleton Instance
media_service = LocalMediaService()