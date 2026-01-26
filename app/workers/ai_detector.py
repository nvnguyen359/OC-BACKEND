# app/workers/ai_detector.py
import os
import sys
import time
import signal
import numpy as np
from multiprocessing import Queue

# --- CẤU HÌNH TỐI ƯU ORANGE PI 3 ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"

# Import OpenCV
try: import cv2
except ImportError: cv2 = None

# Import YOLO (Optional)
try: 
    from ultralytics import YOLO
    import torch
    torch.set_num_threads(1)
except ImportError: 
    YOLO = None

# Import Pyzbar
try:
    from pyzbar import pyzbar
    from pyzbar.pyzbar import ZBarSymbol
except ImportError:
    pyzbar = None

def run_ai_process(input_queue: Queue, output_queue: Queue, model_path: str):
    """
    Tiến trình AI: Tối ưu cho việc đọc mã xa 40cm+ bằng Sharpening & Upscaling.
    """
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI Process] Started. PID: {os.getpid()}")
    
    # 1. Load YOLO (Chỉ dùng detect người)
    model = None
    if YOLO:
        try: 
            model = YOLO(model_path)
            print(f"✅ [AI Process] YOLO Loaded.")
        except Exception as e: 
            print(f"⚠️ [AI Process] YOLO Error: {e}")

    # 2. Ma trận làm nét (Sharpen Kernel) - QUAN TRỌNG CHO MÃ MỜ/XA
    # Giúp làm rõ cạnh các chấm QR code
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

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

            h_input, w_input = img.shape[:2]
            scale_x = target_w / w_input if w_input > 0 else 1.0
            scale_y = target_h / h_input if h_input > 0 else 1.0

            detections = []
            
            # ==================================================================
            # 1. QR CODE / BARCODE (CHIẾN THUẬT ZOOM SỐ & LÀM NÉT)
            # ==================================================================
            if pyzbar and cv2:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                decoded_objects = []
                
                # --- BƯỚC 1: QUÉT NHANH TRÊN ẢNH GỐC ĐÃ LÀM NÉT ---
                # Làm nét ảnh trước khi quét. Giúp đọc được mã ở xa mà không cần crop.
                # Đây là bước quan trọng nhất cho trường hợp của bạn.
                gray_sharp = cv2.filter2D(gray, -1, sharpen_kernel)
                
                decoded_objects = pyzbar.decode(gray_sharp, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                
                # --- BƯỚC 2: NẾU KHÔNG THẤY -> CẮT RỘNG & PHÓNG TO (DIGITAL ZOOM) ---
                # Nếu mã quá nhỏ, ta cắt vùng bàn làm việc (Rộng 90%, Cao 60%)
                # Sau đó phóng to 2 lần (Upscale) để pyzbar nhìn rõ hơn.
                if not decoded_objects:
                    # Cắt vùng rộng hơn (tránh bị mất mã nếu mã nằm lệch như trong ảnh)
                    crop_h_ratio = 0.6  # Lấy 60% chiều cao (vùng giữa)
                    crop_w_ratio = 0.9  # Lấy 90% chiều rộng (gần hết chiều ngang)
                    
                    crop_h = int(h_input * crop_h_ratio)
                    crop_w = int(w_input * crop_w_ratio)
                    
                    # Tọa độ bắt đầu cắt
                    start_y = (h_input - crop_h) // 2
                    start_x = (w_input - crop_w) // 2
                    
                    # Cắt ảnh
                    roi = gray[start_y:start_y+crop_h, start_x:start_x+crop_w]
                    
                    # PHÓNG TO 2 LẦN (Upscale) - Bí quyết đọc mã xa
                    # Mã 40px sẽ thành 80px -> Dễ đọc hơn hẳn
                    roi_zoomed = cv2.resize(roi, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
                    
                    # Làm nét vùng đã phóng to
                    roi_zoomed_sharp = cv2.filter2D(roi_zoomed, -1, sharpen_kernel)
                    
                    # Thử quét trên ảnh phóng to
                    decoded_roi = pyzbar.decode(roi_zoomed_sharp, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                    
                    # Map lại tọa độ từ ảnh phóng to về ảnh gốc
                    for obj in decoded_roi:
                        try:
                            content = obj.data.decode("utf-8")
                            # Tọa độ trên ảnh phóng to
                            zx, zy, zw, zh = obj.rect
                            
                            # Chia 2 để về kích thước vùng cắt
                            real_roi_x = zx // 2
                            real_roi_y = zy // 2
                            real_roi_w = zw // 2
                            real_roi_h = zh // 2
                            
                            # Cộng bù tọa độ cắt để ra tọa độ ảnh gốc
                            final_x = start_x + real_roi_x
                            final_y = start_y + real_roi_y
                            
                            detections.append({
                                "type": "qrcode",
                                "box": [
                                    int(final_x * scale_x), int(final_y * scale_y), 
                                    int(real_roi_w * scale_x), int(real_roi_h * scale_y)
                                ],
                                "label": content,
                                "code": content, 
                                "code_type": obj.type,
                                "color": "#2ecc71"
                            })
                        except: pass
                
                # Nếu bước 1 tìm thấy (trên ảnh gốc làm nét)
                else:
                    for obj in decoded_objects:
                        try:
                            content = obj.data.decode("utf-8")
                            x, y, w, h = obj.rect
                            detections.append({
                                "type": "qrcode",
                                "box": [
                                    int(x * scale_x), int(y * scale_y), 
                                    int(w * scale_x), int(h * scale_y)
                                ],
                                "label": content,
                                "code": content, 
                                "code_type": obj.type,
                                "color": "#2ecc71"
                            })
                        except: pass

            # ==================================================================
            # 2. HUMAN DETECTION (YOLO - GIẢM TẢI)
            # ==================================================================
            if model:
                # Giảm ảnh xuống 320 để nhẹ máy, tập trung CPU cho QR
                results = model.predict(img, imgsz=320, conf=0.5, verbose=False, classes=[0], device='cpu')
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

            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt:
            break
        except Exception: 
            continue
            
    print("🛑 [AI Process] Stopped.")