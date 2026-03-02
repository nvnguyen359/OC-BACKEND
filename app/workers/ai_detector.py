# app/workers/ai_detector.py
import os
import sys
import time
import signal
import urllib.request
import numpy as np
from multiprocessing import Queue

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"

try: 
    import cv2
    print("✅ [AI Check] OpenCV imported successfully.")
except ImportError as e: 
    cv2 = None

try: 
    from ultralytics import YOLO
    import torch
    torch.set_num_threads(1)
    HAS_YOLO = True
except ImportError: 
    YOLO = None
    HAS_YOLO = False

# BẬT LẠI PYZBAR
try:
    from pyzbar import pyzbar
    from pyzbar.pyzbar import ZBarSymbol
    HAS_ZBAR = True
except ImportError:
    pyzbar = None
    HAS_ZBAR = False

def download_wechat_models():
    # Ưu tiên sử dụng model ở ngay thư mục gốc
    if os.path.exists("./detect.prototxt") and os.path.exists("./detect.caffemodel"):
        print("✅ [AI Process] Tìm thấy file model WeChat QR tại thư mục hiện tại.")
        return "./"

    # Nếu không có ở thư mục gốc mới thử tải xuống
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "..", "models", "wechat_qr")
    os.makedirs(model_dir, exist_ok=True)
    base_url = "https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/wechat_qrcode/"
    files = ["detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel"]
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    for file in files:
        file_path = os.path.join(model_dir, file)
        if not os.path.exists(file_path):
            try: 
                urllib.request.urlretrieve(base_url + file, file_path)
            except Exception: 
                return None
    return model_dir

def run_ai_process(input_queue: Queue, output_queue: Queue, model_path: str):
    try: signal.signal(signal.SIGINT, signal.SIG_IGN)
    except: pass

    print(f"🤖 [AI Process] Started. PID: {os.getpid()}")
    
    model = None
    if HAS_YOLO and os.path.exists(model_path):
        try: model = YOLO(model_path)
        except: pass

    wechat_detector = None
    fallback_qr_detector = None
    
    # Khởi tạo bộ cân bằng sáng
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) if cv2 else None
    
    if cv2:
        wechat_model_dir = download_wechat_models()
        if wechat_model_dir:
            p_detect = os.path.join(wechat_model_dir, "detect.prototxt")
            m_detect = os.path.join(wechat_model_dir, "detect.caffemodel")
            p_sr = os.path.join(wechat_model_dir, "sr.prototxt")
            m_sr = os.path.join(wechat_model_dir, "sr.caffemodel")

            if not os.path.exists(p_sr) or not os.path.exists(m_sr):
                p_sr = ""
                m_sr = ""
                
            # [QUAN TRỌNG] Bổ sung 2 dòng này để ÉP TẮT tính năng phóng to (Giảm lag 300% cho Opi3)
            p_sr = ""
            m_sr = ""

            # Thử khởi tạo WeChat QR an toàn
            try:
                # [TỐI ƯU ARM] Truyền p_sr và m_sr rỗng để TẮT mạng Super Resolution (Siêu phân giải).
                if hasattr(cv2, 'wechat_qrcode_WeChatQRCode'):
                    wechat_detector = cv2.wechat_qrcode_WeChatQRCode(p_detect, m_detect, p_sr, m_sr)
                    print("✅ [AI Process] Đã nạp WeChat QR (Chế độ siêu tốc/Tắt SR)!")
                elif hasattr(cv2, 'wechat_qrcode') and hasattr(cv2.wechat_qrcode, 'WeChatQRCode'):
                    wechat_detector = cv2.wechat_qrcode.WeChatQRCode(p_detect, m_detect, p_sr, m_sr)
                    print("✅ [AI Process] Đã nạp WeChat QR (Chế độ siêu tốc/Tắt SR)!")
            except:
                pass # Nuốt lỗi nếu phiên bản OpenCV không tương thích

        # Kích hoạt Fallback nếu WeChat QR không tồn tại
        if wechat_detector is None:
            print("⚠️ [AI Process] Mạch ARM kích hoạt bộ quét dự phòng (Pyzbar 3 Lớp + CV2)!")
            try: fallback_qr_detector = cv2.QRCodeDetector()
            except: pass

    frame_counter = 0     
    last_human_cache = []     

    while True:
        try:
            frame_data = None
            while not input_queue.empty():
                try: frame_data = input_queue.get_nowait()
                except: break
            
            if frame_data is None:
                try: frame_data = input_queue.get(timeout=0.05)
                except: continue
            
            frame_counter += 1
            img = frame_data.get('image')
            cam_id = frame_data.get('cam_id')
            target_w = frame_data.get('target_w', 1280)
            target_h = frame_data.get('target_h', 720)
            
            if img is None: continue

            h_input, w_input = img.shape[:2]
            scale_x = target_w / w_input if w_input > 0 else 1.0
            scale_y = target_h / h_input if h_input > 0 else 1.0

            detections = []
            has_code = False
            
            if cv2:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                # ========================================================
                # [A] WECHAT QR (NẾU ĐÃ CÀI OPENCV-CONTRIB)
                # ========================================================
                if wechat_detector:
                    res, points = wechat_detector.detectAndDecode(gray)
                    if res:
                        for i, content in enumerate(res):
                            if content:
                                has_code = True
                                pts = points[i].astype(int)
                                x, y, w, h = cv2.boundingRect(pts)
                                detections.append({
                                    "type": "qrcode",
                                    "box": [int(x*scale_x), int(y*scale_y), int(w*scale_x), int(h*scale_y)],
                                    "label": content, "code": content, "color": "#2ecc71"
                                })
                
                # ========================================================
                # [B] FALLBACK MODE CHO OPi3 (PYZBAR + CV2 KÈM ZOOM)
                # ========================================================
                else:
                    target_symbols = [ZBarSymbol.QRCODE, ZBarSymbol.CODE128, ZBarSymbol.CODE39, ZBarSymbol.EAN13] if HAS_ZBAR else []
                    
                    # LỚP 1: QUÉT ẢNH GỐC NHANH
                    if HAS_ZBAR:
                        decoded = pyzbar.decode(gray, symbols=target_symbols)
                        for obj in decoded:
                            content = obj.data.decode("utf-8")
                            x, y, w, h = obj.rect
                            has_code = True
                            detections.append({
                                "type": "code",
                                "box": [int(x*scale_x), int(y*scale_y), int(w*scale_x), int(h*scale_y)],
                                "label": content, "code": content, "color": "#3498db"
                            })
                    
                    # LỚP 2: PHÓNG TO VÀ LÀM NÉT
                    if not has_code and (frame_counter % 2 == 0):
                        crop_ratio = 0.6
                        crop_h, crop_w = int(h_input * crop_ratio), int(w_input * crop_ratio)
                        start_y, start_x = (h_input - crop_h) // 2, (w_input - crop_w) // 2
                        
                        roi = gray[start_y:start_y+crop_h, start_x:start_x+crop_w]
                        
                        zoom_factor = 2.0
                        roi_zoomed = cv2.resize(roi, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_CUBIC)
                        
                        kernel_sharpening = np.array([[-1, -1, -1], [-1,  9, -1], [-1, -1, -1]])
                        roi_sharpened = cv2.filter2D(roi_zoomed, -1, kernel_sharpening)
                        
                        roi_enhanced = clahe.apply(roi_sharpened) if clahe else roi_sharpened
                        
                        if HAS_ZBAR:
                            decoded_roi = pyzbar.decode(roi_enhanced, symbols=target_symbols)
                            if not decoded_roi:
                                roi_bin = cv2.adaptiveThreshold(roi_enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4)
                                decoded_roi = pyzbar.decode(roi_bin, symbols=target_symbols)

                            if decoded_roi:
                                for obj in decoded_roi:
                                    content = obj.data.decode("utf-8")
                                    zx, zy, zw, zh = obj.rect
                                    
                                    real_x, real_y = int(zx/zoom_factor), int(zy/zoom_factor)
                                    real_w, real_h = int(zw/zoom_factor), int(zh/zoom_factor)
                                    final_x, final_y = start_x + real_x, start_y + real_y
                                    
                                    has_code = True
                                    detections.append({
                                        "type": "code",
                                        "box": [int(final_x*scale_x), int(final_y*scale_y), int(real_w*scale_x), int(real_h*scale_y)],
                                        "label": content, "code": content, "color": "#3498db"
                                    })
                        
                        if not has_code and fallback_qr_detector:
                            retval, decoded_info, points, _ = fallback_qr_detector.detectAndDecodeMulti(roi_enhanced)
                            if retval and len(decoded_info) > 0:
                                for i, content in enumerate(decoded_info):
                                    if content:
                                        has_code = True
                                        pts = points[i].astype(int)
                                        x, y, w, h = cv2.boundingRect(pts)
                                        
                                        real_x, real_y = int(x/zoom_factor), int(y/zoom_factor)
                                        real_w, real_h = int(w/zoom_factor), int(h/zoom_factor)
                                        final_x, final_y = start_x + real_x, start_y + real_y
                                        
                                        detections.append({
                                            "type": "qrcode",
                                            "box": [int(final_x*scale_x), int(final_y*scale_y), int(real_w*scale_x), int(real_h*scale_y)],
                                            "label": content, "code": content, "color": "#2ecc71"
                                        })

            # ========================================================
            # [C] YOLO HIỆU SUẤT CAO
            # ========================================================
            if model and not has_code:
                if frame_counter % 5 == 0:
                    last_human_cache = [] 
                    try:
                        results = model.predict(img, imgsz=256, conf=0.5, verbose=False, classes=[0], device='cpu')
                        for r in results:
                            for box in r.boxes:
                                x1, y1, x2, y2 = box.xyxy[0].tolist()
                                last_human_cache.append({
                                    "type": "human",
                                    "box": [int(x1*scale_x), int(y1*scale_y), int((x2-x1)*scale_x), int((y2-y1)*scale_y)], 
                                    "label": "Human", "color": "#e74c3c"
                                })
                    except: pass
                
                if last_human_cache: detections.extend(last_human_cache)
            else:
                last_human_cache = []

            if not output_queue.full():
                output_queue.put({'cam_id': cam_id, 'data': detections})

        except KeyboardInterrupt: break
        except Exception: continue
            
    print("🛑 [AI Process] Stopped.")