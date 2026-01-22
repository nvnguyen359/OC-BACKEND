import cv2
import numpy as np

# app/workers/image_processor.py
# Nhiệm vụ: Resize ảnh hiển thị, vẽ Text overlay.
# [TỐI ƯU] Đã loại bỏ các xử lý nặng (CLAHE, Sharpen) khỏi luồng Camera chính để tăng FPS.

class ImageProcessor:
    def __init__(self, font_scale=0.85, thickness=2):
        self.font_scale = font_scale
        self.thickness = thickness
        self.text_color = (255, 255, 255)
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        
        # [LƯU Ý] Đã xóa self.sharpen_kernel và self.clahe ở đây.
        # Lý do: Việc khởi tạo và xử lý chúng trên luồng chính gây nghẽn cổ chai.
        # Chúng sẽ được chuyển sang worker AI.

    def smart_resize(self, frame, target_w, target_h):
        """Resize và crop ảnh vào giữa để vừa khung hình hiển thị"""
        if frame is None or frame.size == 0: return None
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
        [FIX] Chỉ trả về bản copy của frame.
        Không thực hiện CLAHE/Sharpen ở đây để tránh làm chậm Camera Thread 
        và tránh hỏng ảnh (noise) trước khi AI nhận được.
        """
        if frame is None: return None
        # Trả về bản copy để tránh xung đột bộ nhớ khi AI đang xử lý mà Camera lại ghi đè
        return frame.copy()

    def draw_text(self, frame, text, x, y, color=None):
        if color is None: color = self.text_color
        try:
            font = cv2.FONT_HERSHEY_SIMPLEX
            # Vẽ viền đen (thickness + 3) để chữ nổi bật trên nền sáng
            cv2.putText(frame, text, (x, y), font, self.font_scale, (0, 0, 0), self.thickness + 3, cv2.LINE_AA)
            # Vẽ chữ chính
            cv2.putText(frame, text, (x, y), font, self.font_scale, color, self.thickness, cv2.LINE_AA)
        except: pass

    def to_jpeg(self, frame):
        try:
            _, enc = cv2.imencode(".jpg", frame, self.encode_param)
            return enc.tobytes() if enc is not None else None
        except: return None