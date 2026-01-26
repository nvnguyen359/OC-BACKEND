import cv2
import numpy as np
import time
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol

def test_on_windows():
    # 1. Mở Camera
    cap = cv2.VideoCapture(0)
    
    # Ép độ phân giải về HD 720p (Giống môi trường Orange Pi)
    # Để đảm bảo test trên Windows sát với thực tế nhất
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # 2. Chuẩn bị công cụ ảnh (Chỉ khởi tạo 1 lần)
    # CLAHE: Cân bằng sáng (Giúp mã QR nổi bật trên nền giấy vận đơn)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    # Kernel làm nét
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

    # Đo FPS
    prev_time = 0

    print("🚀 Đang chạy trên Windows. Nhấn 'q' để thoát.")
    print("🎯 Chế độ: SNIPER SCOPE (Chỉ xử lý vùng tâm để đọc xa & giảm lag)")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Tính FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
        prev_time = curr_time

        h_orig, w_orig = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # =====================================================================
        # 🟢 LOGIC "KÍNH NGẮM" (SNIPER SCOPE)
        # =====================================================================
        
        # 1. CẮT VÙNG TÂM (480x480)
        # Thay vì xử lý cả ảnh 1280x720 (921.600 pixel)
        # Ta chỉ xử lý 480x480 (230.400 pixel) -> Nhẹ hơn gấp 4 lần!
        sniper_size = 480
        if h_orig < sniper_size: sniper_size = h_orig

        start_y = (h_orig - sniper_size) // 2
        start_x = (w_orig - sniper_size) // 2
        
        # Lấy vùng ngắm (ROI)
        roi = gray[start_y : start_y+sniper_size, start_x : start_x+sniper_size]

        # 2. XỬ LÝ VÙNG NGẮM (Zoom + Tăng nét)
        # Zoom 1.5x (Đủ để đọc mã ở 40cm)
        roi_zoom = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
        
        # Tăng tương phản (Quan trọng cho vận đơn mờ)
        roi_enhanced = clahe.apply(roi_zoom)
        
        # Làm nét cạnh
        roi_final = cv2.filter2D(roi_enhanced, -1, sharpen_kernel)

        # 3. QUÉT MÃ TRÊN VÙNG ĐÃ XỬ LÝ
        decoded_objects = pyzbar.decode(roi_final, symbols=[ZBarSymbol.CODE128, ZBarSymbol.QRCODE])
        
        # =====================================================================
        # 🖌️ VẼ GIAO DIỆN DEBUG
        # =====================================================================
        
        # Vẽ khung "Kính Ngắm" màu vàng để người dùng biết chỗ đặt hàng
        cv2.rectangle(frame, (start_x, start_y), (start_x+sniper_size, start_y+sniper_size), (0, 255, 255), 2)
        cv2.putText(frame, "SNIPER ZONE (40cm+)", (start_x, start_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if decoded_objects:
            for obj in decoded_objects:
                content = obj.data.decode("utf-8")
                
                # Map tọa độ từ vùng Zoom về màn hình chính
                zx, zy, zw, zh = obj.rect
                
                # Công thức: (Tọa độ Zoom / 1.5) + Tọa độ Cắt
                real_x = int(start_x + (zx / 1.5))
                real_y = int(start_y + (zy / 1.5))
                real_w = int(zw / 1.5)
                real_h = int(zh / 1.5)

                # Vẽ khung xanh lá khi nhận diện được
                cv2.rectangle(frame, (real_x, real_y), (real_x+real_w, real_y+real_h), (0, 255, 0), 3)
                
                # Hiển thị nội dung mã
                cv2.rectangle(frame, (real_x, real_y - 30), (real_x + len(content)*14, real_y), (0, 255, 0), -1)
                cv2.putText(frame, content, (real_x + 5, real_y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                print(f"✅ QUÉT ĐƯỢC: {content}")

        # Hiển thị FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Hiển thị cửa sổ
        # Cửa sổ 1: Màn hình chính
        cv2.imshow("TEST WINDOWS - MAIN", frame)
        
        # Cửa sổ 2: Những gì AI thực sự nhìn thấy (Đã zoom & tăng sáng)
        # Bạn nhìn vào đây để biết tại sao nó đọc được
        cv2.imshow("TEST WINDOWS - AI EYE", roi_final)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_on_windows()