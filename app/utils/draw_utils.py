import cv2
from datetime import datetime

def put_text_with_outline(img, text, x, y, font_scale=0.8, thickness=2, color=(255, 255, 255)):
    """
    Vẽ chữ có viền đen để nổi bật.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 1. Vẽ viền đen (dày hơn)
    cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
    # 2. Vẽ lõi màu (mặc định trắng)
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_timestamp_and_code(frame, order_code=None):
    """
    Vẽ thời gian thực và mã đơn hàng (nếu đang quay).
    """
    if frame is None:
        return None
        
    h, w = frame.shape[:2]
    
    # --- 1. Vẽ Thời gian (Góc trên trái) ---
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    put_text_with_outline(frame, now, 20, 40, font_scale=0.8, thickness=2)

    # --- 2. Vẽ Mã đơn (Góc dưới phải - Chỉ khi đang quay) ---
    if order_code:
        text = f"REC: {order_code}"
        # Tính toán vị trí để căn lề phải
        (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        text_x = w - text_w - 20
        text_y = h - 20
        
        # Vẽ màu đỏ (BGR: 0, 0, 255) để cảnh báo đang Ghi hình
        put_text_with_outline(frame, text, text_x, text_y, font_scale=1.0, thickness=2, color=(0, 0, 255))
    
    return frame