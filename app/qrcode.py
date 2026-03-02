import cv2
import threading
import time
import os
import sys
import platform
from pyzbar import pyzbar

# ==========================================
# 1. NHẬN DẠNG HỆ ĐIỀU HÀNH
# ==========================================
OS_NAME = platform.system()
IS_WINDOWS = (OS_NAME == "Windows")
IS_LINUX = (OS_NAME == "Linux")

print(f"Hệ thống nhận diện OS: {OS_NAME}")
if IS_WINDOWS:
    print("-> Kích hoạt chế độ UI (Có màn hình, vẽ khung, dùng phím 'q' để thoát)")
elif IS_LINUX:
    print("-> Kích hoạt chế độ Headless cho OPi3 (Không màn hình, tối ưu CPU, dùng Ctrl+C để thoát)")
else:
    print("-> OS không xác định, mặc định chạy chế độ Headless.")
    IS_LINUX = True

# ==========================================
# 2. KHỞI TẠO WECHAT QR
# ==========================================
model_dir = "./"
try:
    detector = cv2.wechat_qrcode_WeChatQRCode(
        os.path.join(model_dir, "detect.prototxt"),
        os.path.join(model_dir, "detect.caffemodel"),
        os.path.join(model_dir, "sr.prototxt"),
        os.path.join(model_dir, "sr.caffemodel")
    )
except Exception as e:
    print(f"Lỗi tải model WeChat QR: {e}")
    sys.exit(1)

# ==========================================
# 3. LỚP CAMERA ĐA NỀN TẢNG (AUTO-DETECT)
# ==========================================
class SmartCamera:
    def __init__(self):
        # Tự động dò tìm camera đang hoạt động thay vì fix cứng src=0
        self.cap = self._find_working_camera()
        
        if self.cap is None:
            print("Không thể kết nối Camera! Vui lòng kiểm tra lại cáp hoặc chạy lệnh 'ls /dev/video*'")
            sys.exit(1)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.ret, self.frame = self.cap.read()
        self.stopped = False
    def _find_working_camera(self):
        # OPi3 chỉ có 1 cam, ta ưu tiên test index 1 (cổng hình ảnh) và 3 (cổng metadata)
        test_indices = [1, 3, 0, 2] if IS_LINUX else [0, 1, 2, 3]
        
        for index in test_indices:
            print(f"Đang thử kết nối camera tại index {index}...")
            if IS_WINDOWS:
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(index, cv2.CAP_V4L2)

            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                if IS_LINUX:
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))

                print("Đang đọc thử 5 frames để kiểm tra luồng ảnh...")
                valid_frame = False
                last_frame = None
                
                for _ in range(5):
                    ret, frame = cap.read()
                    if ret and frame is not None and frame.any():
                        valid_frame = True
                        last_frame = frame
                    time.sleep(0.1)

                if valid_frame and last_frame is not None:
                    print(f"-> THÀNH CÔNG: Đã kết nối Camera tại index {index}!")
                    
                    # [MỚI] Lưu ảnh ra file để kiểm tra thực tế
                    img_path = os.path.join(os.getcwd(), f"test_cam_index_{index}.jpg")
                    cv2.imwrite(img_path, last_frame)
                    print(f"-> ĐÃ CHỤP ẢNH THỬ: Kiểm tra file '{img_path}' xem có hình thật không nhé!")
                    
                    return cap
                else:
                    print(f"-> Index {index} mở được nhưng ảnh rỗng/đen. Bỏ qua.")
                    cap.release()
            else:
                print(f"-> Không thể mở index {index}.")
                
        return None

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
            if IS_LINUX:
                time.sleep(0.01) # Tránh full load 1 nhân CPU trên OPi3

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

# ==========================================
# 4. CHẠY HỆ THỐNG
# ==========================================
# Đã bỏ tham số src=0, để class tự dò tìm
cam = SmartCamera().start()
print("-" * 50)
print("Hệ thống đã sẵn sàng quét mã!")

last_scanned_data = ""
last_scanned_time = 0
DEBOUNCE_TIME = 2.0 # Giây (Chống lặp kết quả)

try:
    while True:
        img = cam.read()
        if img is None: 
            time.sleep(0.1)
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        current_time = time.time()

        # Quét QR (WeChat QR)
        res, points = detector.detectAndDecode(gray)
        if res:
            for i, data in enumerate(res):
                if data and (data != last_scanned_data or current_time - last_scanned_time > DEBOUNCE_TIME):
                    print(f"[{time.strftime('%H:%M:%S')}] [QR] {data}")
                    last_scanned_data = data
                    last_scanned_time = current_time
                
                # Chỉ vẽ khung nếu ở Windows
                if IS_WINDOWS and points is not None:
                    pts = points[i].astype(int)
                    for j in range(4):
                        cv2.line(img, tuple(pts[j]), tuple(pts[(j+1)%4]), (0, 255, 0), 2)

        # Quét Barcode (PyZbar)
        barcodes = pyzbar.decode(gray)
        for barcode in barcodes:
            if barcode.type != 'QRCODE': 
                b_data = barcode.data.decode("utf-8")
                if b_data != last_scanned_data or current_time - last_scanned_time > DEBOUNCE_TIME:
                    print(f"[{time.strftime('%H:%M:%S')}] [Barcode - {barcode.type}] {b_data}")
                    last_scanned_data = b_data
                    last_scanned_time = current_time
                
                # Chỉ vẽ khung nếu ở Windows
                if IS_WINDOWS:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Xử lý giao diện & Thoát chương trình
        if IS_WINDOWS:
            cv2.imshow("Smart Scanner (Windows Mode)", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Trên Linux, vòng lặp chạy tối đa tốc độ nhưng ta cho nghỉ 1 chút để tiết kiệm tài nguyên
            time.sleep(0.01) 

except KeyboardInterrupt:
    print("\nĐã nhận lệnh dừng từ người dùng...")

finally:
    print("Đang giải phóng Camera...")
    cam.stop()
    if IS_WINDOWS:
        cv2.destroyAllWindows()
    print("Hệ thống đã tắt an toàn.")