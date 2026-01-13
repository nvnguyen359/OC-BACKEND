# app/workers/ai_detector.py
import os
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"

import time
import cv2
import numpy as np
from multiprocessing import Queue
import signal

try: from ultralytics import YOLO
except ImportError: YOLO = None

try:
    from pyzbar import pyzbar
    from pyzbar.pyzbar import ZBarSymbol
except ImportError:
    pyzbar = None

def run_ai_process(input_queue: Queue, output_queue: Queue, model_path: str):
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI WORKER] Starting... Model: {model_path}")
    
    model = None
    if YOLO:
        try: 
            model = YOLO(model_path)
            print("✅ [AI WORKER] YOLO Loaded.")
        except: pass

    while True:
        try:
            frame_data = input_queue.get(timeout=0.1)
            img = frame_data['image']
            cam_id = frame_data['cam_id']
            
            detections = []

            # 1. HUMAN DETECT
            if model:
                results = model.predict(img, imgsz=320, conf=0.5, verbose=False)
                for r in results:
                    for box in r.boxes:
                        if int(box.cls[0]) == 0: # Class 0 là Person
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            
                            # [SỬA LỖI BỊ LỆCH TẠI ĐÂY]
                            # Phải dùng phép trừ để ra Chiều Rộng và Chiều Cao
                            w = int(x2 - x1)
                            h = int(y2 - y1)
                            x = int(x1)
                            y = int(y1)

                            detections.append({
                                "type": "human",
                                "box": [x, y, w, h], # Gửi w, h (đã trừ)
                                "label": f"Person {int(box.conf[0]*100)}%",
                                "color": "#e74c3c"
                            })

            # 2. QR CODE
            if pyzbar:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                decoded = pyzbar.decode(gray, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
                if not decoded:
                    # Thử tăng sáng nếu không đọc được
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    decoded = pyzbar.decode(clahe.apply(gray), symbols=[ZBarSymbol.QRCODE])

                for obj in decoded:
                    code = obj.data.decode("utf-8")
                    x, y, w, h = obj.rect
                    detections.append({
                        "type": "qrcode",
                        "box": [x, y, w, h],
                        "label": code,
                        "color": "#2ecc71"
                    })

            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt: break
        except Exception: continue