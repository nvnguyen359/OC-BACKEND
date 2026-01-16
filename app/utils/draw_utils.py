# app/utils/draw_utils.py
import cv2
from datetime import datetime
import pytz # Import thư viện múi giờ (đã có trong requirements của bạn)

def put_text_with_outline(img, text, x, y, font_scale=0.8, thickness=2, color=(255, 255, 255)):
    """
    Vẽ chữ có viền đen để nổi bật trên mọi nền.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 1. Vẽ viền đen (dày hơn một chút)
    cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
    # 2. Vẽ lõi màu (mặc định trắng)
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_timestamp_and_code(frame, order_code=None):
    """
    - Mã đơn: Góc trên TRÁI (Nếu có)
    - Thời gian: Góc trên PHẢI (Giờ Việt Nam)
    """
    if frame is None:
        return None
        
    h, w = frame.shape[:2]
    
    # --- 1. Vẽ Thời gian (Góc trên PHẢI) ---
    # Lấy giờ VN chuẩn xác
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now_str = datetime.now(vn_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    # Tính toán độ rộng chữ để căn phải
    font_scale = 0.7
    thickness = 2
    (text_w, text_h), _ = cv2.getTextSize(now_str, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    
    x_time = w - text_w - 20 # Cách lề phải 20px
    y_time = 30              # Cách lề trên 30px
    
    put_text_with_outline(frame, now_str, x_time, y_time, font_scale, thickness)

    # --- 2. Vẽ Mã đơn (Góc trên TRÁI - Chỉ khi có đơn) ---
    if order_code:
        text = f"REC: {order_code}"
        # Vẽ màu ĐỎ để cảnh báo đang xử lý đơn
        put_text_with_outline(frame, text, 20, 30, font_scale=0.8, thickness=2, color=(0, 0, 255))
    
    return frame