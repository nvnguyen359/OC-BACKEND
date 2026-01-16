# app/workers/ai_detector.py
import os
import sys
import time
import signal
import numpy as np
from multiprocessing import Queue

# Cấu hình môi trường
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"

# Import OpenCV
try: import cv2
except ImportError: cv2 = None

# Import YOLO (Optional)
try: from ultralytics import YOLO
except ImportError: YOLO = None

# Import Pyzbar (Optional)
try:
    from pyzbar import pyzbar
    from pyzbar.pyzbar import ZBarSymbol
except ImportError:
    pyzbar = None

def run_ai_process(input_queue: Queue, output_queue: Queue, model_path: str):
    """
    Tiến trình AI chạy độc lập (Process).
    Nhận ảnh từ input_queue -> Xử lý -> Đẩy kết quả vào output_queue.
    """
    
    # [NÂNG CẤP 1] Bỏ qua tín hiệu Ctrl+C (SIGINT)
    # Để Process cha (Main) tự quản lý việc tắt/bật process này.
    # Giúp tránh lỗi "KeyboardInterrupt" rác in ra màn hình.
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI Process] Started. PID: {os.getpid()}")
    
    # Load Model
    model = None
    if YOLO:
        try: 
            # Load model nhẹ (nếu có file)
            model = YOLO(model_path)
            print(f"✅ [AI Process] YOLO Model '{model_path}' Loaded.")
        except Exception as e: 
            print(f"⚠️ [AI Process] YOLO Error: {e}")

    if not pyzbar:
        print("⚠️ [AI Process] Pyzbar not found. QR scanning disabled.")

    while True:
        try:
            # Lấy dữ liệu từ Queue (Timeout ngắn để không block cứng)
            # data format: {'cam_id': 1, 'image': np_array, 'scale': 1.0}
            frame_data = input_queue.get(timeout=0.1)
            
            img = frame_data.get('image')
            cam_id = frame_data.get('cam_id')
            
            if img is None: continue

            detections = []

            # ==========================================
            # 1. HUMAN DETECTION (YOLO)
            # ==========================================
            if model:
                # Chỉ detect class 0 (person)
                results = model.predict(img, imgsz=640, conf=0.4, verbose=False, classes=[0])
                for r in results:
                    for box in r.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detections.append({
                            "type": "human",
                            "box": [int(x1), int(y1), int(x2-x1), int(y2-y1)], 
                            "label": f"Human {int(box.conf[0]*100)}%",
                            "color": "#e74c3c" # Red
                        })

            # ==========================================
            # 2. QR/BARCODE DETECTION (Pyzbar)
            # ==========================================
            if pyzbar:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Decode QR & Barcode (Code128 thường dùng cho vận đơn)
                decoded = pyzbar.decode(gray, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                
                # Nếu không thấy, thử tăng tương phản (CLAHE)
                if not decoded:
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    decoded = pyzbar.decode(clahe.apply(gray), symbols=[ZBarSymbol.QRCODE])

                for obj in decoded:
                    try:
                        code_content = obj.data.decode("utf-8")
                        x, y, w, h = obj.rect
                        
                        detections.append({
                            "type": "qrcode",
                            "box": [x, y, w, h],
                            "label": code_content,
                            # [QUAN TRỌNG] Các key này được CameraWorker dùng để Auto-Sync
                            "code": code_content, 
                            "code_type": obj.type,
                            "color": "#2ecc71" # Green
                        })
                    except: pass

            # Gửi kết quả về lại cho Worker
            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt:
            # Trường hợp hiếm hoi bắt được signal
            break
        except Exception: 
            # Nếu Queue rỗng (Empty) hoặc lỗi xử lý ảnh -> Bỏ qua, tiếp tục loop
            continue
            
    print("🛑 [AI Process] Stopped.")