# app/workers/ai_detector.py
import os
import sys
import time
import signal
import numpy as np
from multiprocessing import Queue

# Cấu hình môi trường: Tắt log rác của OpenCV
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
    Tiến trình AI chạy độc lập.
    Nhiệm vụ: Phát hiện người (YOLO) & Giải mã QR/Barcode (Pyzbar Multi-pass).
    """
    
    # Bỏ qua tín hiệu Ctrl+C để tiến trình cha quản lý việc dừng
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI Process] Started. PID: {os.getpid()}")
    
    # 1. Load YOLO Model
    model = None
    if YOLO:
        try: 
            # Load model, chuyển sang CPU nếu không có GPU
            model = YOLO(model_path)
            print(f"✅ [AI Process] YOLO Model '{model_path}' Loaded.")
        except Exception as e: 
            print(f"⚠️ [AI Process] YOLO Error: {e}")

    # 2. Khởi tạo công cụ xử lý ảnh
    clahe = None
    if cv2 is not None:
        # CLAHE giúp cân bằng sáng cục bộ, tốt cho mã bị tối góc
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    while True:
        try:
            try:
                frame_data = input_queue.get(timeout=0.1)
            except:
                continue
            
            img = frame_data.get('image')
            cam_id = frame_data.get('cam_id')
            target_w = frame_data.get('target_w', 1280)
            target_h = frame_data.get('target_h', 720)
            
            if img is None: continue

            # Tính tỷ lệ scale
            h_input, w_input = img.shape[:2]
            scale_x = target_w / w_input if w_input > 0 else 1.0
            scale_y = target_h / h_input if h_input > 0 else 1.0

            detections = []

            # ==================================================================
            # 1. HUMAN DETECTION (YOLO)
            # ==================================================================
            if model:
                # imgsz=480 giúp tăng tốc độ xử lý trên Orange Pi
                results = model.predict(img, imgsz=480, conf=0.45, verbose=False, classes=[0], device='cpu')
                for r in results:
                    for box in r.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detections.append({
                            "type": "human",
                            "box": [
                                int(x1 * scale_x), int(y1 * scale_y), 
                                int((x2 - x1) * scale_x), int((y2 - y1) * scale_y)
                            ], 
                            "label": f"Human {int(box.conf[0]*100)}%",
                            "color": "#e74c3c"
                        })

            # ==================================================================
            # 2. QR CODE / BARCODE DETECTION (Chiến thuật 4 Lớp)
            # [FIX] Tối ưu hóa để chống chói và ánh sáng mạnh
            # ==================================================================
            if pyzbar and cv2:
                # Chuyển ảnh xám
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                decoded = []

                # --- Lớp 1: Ảnh gốc (Nhanh nhất) ---
                # Dành cho trường hợp ánh sáng hoàn hảo
                decoded = pyzbar.decode(gray, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                
                # --- Lớp 2: Adaptive Threshold (Chống Chói/Bóng) ---
                # [QUAN TRỌNG] Cái này fix lỗi bật đèn của bạn.
                # Nó tính ngưỡng riêng cho từng vùng nhỏ, giúp đọc được mã dù nền bị sáng rực.
                if not decoded:
                    gray_adaptive = cv2.adaptiveThreshold(
                        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                        cv2.THRESH_BINARY, 21, 10
                    )
                    decoded = pyzbar.decode(gray_adaptive, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

                # --- Lớp 3: Otsu's Binarization (Tự động tìm ngưỡng) ---
                # Thay thế cho ngưỡng cứng 90. Otsu tự tìm ngưỡng tối ưu (ví dụ 120, 150)
                # Dành cho trường hợp độ tương phản thấp.
                if not decoded:
                    _, gray_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    decoded = pyzbar.decode(gray_otsu, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

                # --- Lớp 4: CLAHE (Tăng tương phản) ---
                # Dành cho trường hợp mã nằm trong bóng tối hoặc góc khuất
                if not decoded and clahe:
                    gray_clahe = clahe.apply(gray)
                    # Sau khi tăng tương phản thì Otsu lại một lần nữa
                    _, gray_clahe_otsu = cv2.threshold(gray_clahe, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    decoded = pyzbar.decode(gray_clahe_otsu, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])

                # --- Xử lý kết quả giải mã ---
                for obj in decoded:
                    try:
                        code_content = obj.data.decode("utf-8")
                        x, y, w, h = obj.rect
                        
                        detections.append({
                            "type": "qrcode",
                            "box": [
                                int(x * scale_x), int(y * scale_y), 
                                int(w * scale_x), int(h * scale_y)
                            ],
                            "label": code_content,
                            "code": code_content, 
                            "code_type": obj.type,
                            "color": "#2ecc71"
                        })
                    except: pass

            # Trả kết quả
            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt:
            break
        except Exception: 
            continue
            
    print("🛑 [AI Process] Stopped.")