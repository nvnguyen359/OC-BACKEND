import cv2

# Chọn index camera (0 hoặc 1, 2...)
CAM_INDEX = 0

def nothing(x): pass

cap = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW) # Thêm cv2.CAP_DSHOW nếu chạy Windows
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow('Cam Tuner')

# Tạo thanh trượt
# Exposure: Thường là số âm (-1 đến -10) hoặc số dương tùy Driver camera
cv2.createTrackbar('Exposure', 'Cam Tuner', 0, 20, nothing) 
cv2.createTrackbar('Brightness', 'Cam Tuner', 128, 255, nothing)
cv2.createTrackbar('Contrast', 'Cam Tuner', 32, 255, nothing)
cv2.createTrackbar('Gain', 'Cam Tuner', 0, 255, nothing) # ISO giả lập

# Tắt Auto Focus nếu có thể (0: Manual, 1: Auto)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) 

while True:
    # Đọc giá trị từ thanh trượt
    exp = cv2.getTrackbarPos('Exposure', 'Cam Tuner')
    bri = cv2.getTrackbarPos('Brightness', 'Cam Tuner')
    con = cv2.getTrackbarPos('Contrast', 'Cam Tuner')
    gain = cv2.getTrackbarPos('Gain', 'Cam Tuner')

    # Set giá trị cho Camera (Lưu ý: Exposure trên OpenCV thường hoạt động hơi lạ tùy Cam)
    # Giá trị Exposure thực tế thường là -1, -2, -3... (trên Windows)
    # Hoặc 100, 200... (trên Linux V4L2)
    # Bạn thử điều chỉnh cách tính toán này:
    
    # Ví dụ set Exposure (Thử nghiệm):
    # cap.set(cv2.CAP_PROP_EXPOSURE, -exp) 
    
    cap.set(cv2.CAP_PROP_BRIGHTNESS, bri)
    cap.set(cv2.CAP_PROP_CONTRAST, con)
    # cap.set(cv2.CAP_PROP_GAIN, gain)

    ret, frame = cap.read()
    if not ret: break

    # Giả lập bộ lọc AI của chúng ta để xem kết quả cuối
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    cv2.imshow('Cam Tuner (Original)', frame)
    cv2.imshow('AI Input (Gray + CLAHE)', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()