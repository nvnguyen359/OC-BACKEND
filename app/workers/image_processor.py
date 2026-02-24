import cv2
import numpy as np

# app/workers/image_processor.py
# Nhiệm vụ: Resize ảnh hiển thị, vẽ Text overlay.
# [TỐI ƯU CHO OPI3]: Sử dụng ảnh xám (Grayscale) kết hợp kernel làm nét siêu nhẹ.

class ImageProcessor:
    def __init__(self, font_scale=0.85, thickness=2):
        self.font_scale = font_scale
        self.thickness = thickness
        self.text_color = (255, 255, 255)
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        
        # Ma trận làm nét (Sharpen) siêu nhẹ.
        # Chạy rất nhanh trên các thiết bị nhúng như Orange Pi.
        self.fast_sharpen_kernel = np.array([
            [0, -1, 0], 
            [-1, 5, -1], 
            [0, -1, 0]
        ], dtype=np.float32)

    def smart_resize(self, frame, target_w, target_h):
        """Resize và crop ảnh vào giữa để vừa khung hình hiển thị"""
        if frame is None or frame.size == 0: return None
        
        # [BẢO VỆ TỪ CAMERA] Đảm bảo ảnh gốc luôn là 3 kênh màu trước khi xử lý
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif len(frame.shape) == 3 and frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
        h, w = frame.shape[:2]
        if h == target_h and w == target_w: return frame

        src_ratio = w / h
        target_ratio = target_w / target_h

        if src_ratio > target_ratio:
            scale = target_h / h
            new_w = int(w * scale)
            new_h = target_h
            resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            start_x = (new_w - target_w) // 2
            return resized[:, start_x : start_x + target_w]
        else:
            scale = target_w / w
            new_w = target_w
            new_h = int(h * scale)
            resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            start_y = (new_h - target_h) // 2
            return resized[start_y : start_y + target_h, :]

    def preprocess_for_ai(self, frame):
        """
        [FIX CHO OPI3]
        - Khung hình gửi đi xem trực tiếp vẫn có màu và mượt.
        - Khung hình gửi cho AI sẽ bị chuyển thành Đen Trắng và làm sắc nét.
        """
        if frame is None: return None
        
        try:
            # 1. Tránh ghi đè lên frame đang hiển thị
            ai_frame = frame.copy()
            
            # 2. Ép sang Đen Trắng (Grayscale). 
            # Giúp AI đọc QR tốt hơn và giảm thời gian filter2D đi 3 lần!
            gray_frame = cv2.cvtColor(ai_frame, cv2.COLOR_BGR2GRAY)
            
            # 3. Làm nét ảnh (Chống mờ nhòe do camera Opi3)
            sharpened_frame = cv2.filter2D(gray_frame, -1, self.fast_sharpen_kernel)
            
            # 4. [FIX LỖI CRASH] "Lừa" YOLO và Pyzbar bằng cách nhân bản lên 3 kênh
            final_ai_frame = cv2.cvtColor(sharpened_frame, cv2.COLOR_GRAY2BGR)
            
            return final_ai_frame
        except:
            # Fallback nếu có lỗi bất ngờ
            return frame.copy()

    def draw_text(self, frame, text, x, y, color=None):
        if color is None: color = self.text_color
        try:
            font = cv2.FONT_HERSHEY_SIMPLEX
            # Vẽ viền đen (thickness + 3) để chữ nổi bật trên nền sáng
            cv2.putText(frame, text, (x, y), font, self.font_scale, (0, 0, 0), self.thickness + 1, cv2.LINE_AA)
            # Vẽ chữ chính
            cv2.putText(frame, text, (x, y), font, self.font_scale, color, self.thickness, cv2.LINE_AA)
        except: pass

    def to_jpeg(self, frame):
        try:
            _, enc = cv2.imencode(".jpg", frame, self.encode_param)
            return enc.tobytes() if enc is not None else None
        except: return None