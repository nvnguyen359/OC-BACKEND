# app/workers/ai_detector.py
import os
import sys
import time
import signal
import numpy as np
from multiprocessing import Queue

# --- CẤU HÌNH HỆ THỐNG ---
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"

# 1. IMPORT OPENCV
try: 
    import cv2
    print("✅ [AI Check] OpenCV imported successfully.")
except ImportError as e: 
    cv2 = None
    print(f"❌ [AI Check] OpenCV MISSING: {e}")

# 2. IMPORT YOLO (HUMAN DETECTION)
try: 
    from ultralytics import YOLO
    import torch
    torch.set_num_threads(1)
    HAS_YOLO = True
    print("✅ [AI Check] Ultralytics (YOLO) imported successfully.")
except ImportError as e: 
    YOLO = None
    HAS_YOLO = False
    print(f"❌ [AI Check] Ultralytics MISSING (No Human Detect): {e}")

# 3. IMPORT PYZBAR (QR/BARCODE)
try:
    from pyzbar import pyzbar
    from pyzbar.pyzbar import ZBarSymbol
    HAS_ZBAR = True
    print("✅ [AI Check] Pyzbar imported successfully.")
except ImportError as e:
    pyzbar = None
    HAS_ZBAR = False
    print(f"❌ [AI Check] Pyzbar MISSING. Run 'apt install libzbar0'. Error: {e}")

def run_ai_process(input_queue: Queue, output_queue: Queue, model_path: str):
    """
    Tiến trình AI độc lập: Xử lý QR Code và Phát hiện người (Human Detection)
    """
    # Bỏ qua tín hiệu Interrupt để tiến trình cha (Main) quản lý việc đóng
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI Process] Started. PID: {os.getpid()}")
    
    # --- LOAD MODEL YOLO ---
    model = None
    if HAS_YOLO:
        if os.path.exists(model_path):
            try: 
                model = YOLO(model_path)
                print(f"✅ [AI Process] YOLO Model Loaded: {model_path}")
            except Exception as e: 
                print(f"❌ [AI Process] Failed to load YOLO: {e}")
        else:
            print(f"❌ [AI Process] Weights not found: {model_path}")

    # Ma trận làm nét ảnh (Laplacian-based sharpen)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    
    # Khởi tạo bộ cân bằng ánh sáng cục bộ (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) if cv2 else None

    while True:
        try:
            try:
                # Lấy dữ liệu từ hàng đợi (timeout để tránh treo tiến trình)
                frame_data = input_queue.get(timeout=0.1)
            except:
                continue
            
            img = frame_data.get('image')
            cam_id = frame_data.get('cam_id')
            target_w = frame_data.get('target_w', 1280)
            target_h = frame_data.get('target_h', 720)
            
            if img is None: continue

            # Tính toán tỉ lệ scale để trả về tọa độ chính xác cho UI
            h_input, w_input = img.shape[:2]
            scale_x = target_w / w_input if w_input > 0 else 1.0
            scale_y = target_h / h_input if h_input > 0 else 1.0

            detections = []
            
            # ------------------------------------------------------------------
            # 1. XỬ LÝ QUÉT MÃ (QR CODE & BARCODE)
            # ------------------------------------------------------------------
            if HAS_ZBAR and cv2:
                try:
                    # Chuyển xám và tăng cường độ tương phản
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    gray_enhanced = clahe.apply(gray) if clahe else gray
                    
                    # Làm nét để các vạch mã rõ ràng hơn
                    gray_sharp = cv2.filter2D(gray_enhanced, -1, sharpen_kernel)
                    
                    # Thử quét lần 1: Toàn màn hình
                    decoded_objects = pyzbar.decode(gray_sharp, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                    
                    # Nếu không thấy -> Thử Zoom 1.5x vùng trung tâm (giữ nguyên tỉ lệ)
                    if not decoded_objects:
                        crop_h, crop_w = int(h_input * 0.7), int(w_input * 0.7)
                        start_y, start_x = (h_input - crop_h) // 2, (w_input - crop_w) // 2
                        
                        roi = gray_enhanced[start_y:start_y+crop_h, start_x:start_x+crop_w]
                        
                        # Phóng to vùng trung tâm bằng nội suy Cubic để giữ độ sắc nét
                        roi_zoomed = cv2.resize(roi, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
                        roi_zoomed_sharp = cv2.filter2D(roi_zoomed, -1, sharpen_kernel)
                        
                        decoded_roi = pyzbar.decode(roi_zoomed_sharp, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                        
                        for obj in decoded_roi:
                            content = obj.data.decode("utf-8")
                            zx, zy, zw, zh = obj.rect
                            
                            # Map tọa độ từ ảnh Zoom về ảnh gốc ban đầu
                            real_roi_x, real_roi_y = int(zx / 1.5), int(zy / 1.5)
                            real_roi_w, real_roi_h = int(zw / 1.5), int(zh / 1.5)
                            
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
                                "code_type": str(obj.type),
                                "color": "#2ecc71"
                            })
                    else:
                        # Kết quả quét toàn màn hình thành công
                        for obj in decoded_objects:
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
                                "code_type": str(obj.type),
                                "color": "#2ecc71"
                            })
                except Exception as e:
                    print(f"⚠️ [AI QR] Scan Error: {e}")

            # ------------------------------------------------------------------
            # 2. XỬ LÝ PHÁT HIỆN NGƯỜI (HUMAN DETECTION)
            # ------------------------------------------------------------------
            if model:
                try:
                    # Predict với imgsz nhỏ để tăng tốc độ trên CPU (Orange Pi/PC)
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
                except Exception as e:
                    print(f"⚠️ [AI YOLO] Error: {e}")

            # Gửi toàn bộ metadata phát hiện được về Main Process
            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt:
            break
        except Exception as e: 
            print(f"⚠️ [AI Process] Loop Error: {e}")
            continue
            
    print("🛑 [AI Process] Stopped.")