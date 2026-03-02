# app/workers/camera_stream.py
import cv2
import time
import platform
import os
import sys
import threading

# KHÓA TOÀN CỤC ĐỂ TRÁNH XUNG ĐỘT PHẦN CỨNG ĐA LUỒNG
_global_cam_lock = threading.Lock()

class FailsafeSuppressStderr:
    """Class giúp ẩn log rác của OpenCV/FFmpeg trên Linux"""
    def __enter__(self):
        try: sys.stderr.flush()
        except: pass
    def __exit__(self, exc_type, exc_value, traceback): pass

class CameraStream:
    def __init__(self, source, cam_id):
        self.source = source
        self.cam_id = cam_id
        # Chuyển đổi sang int nếu là chuỗi số (ví dụ "0" -> 0)
        if isinstance(self.source, str) and self.source.isdigit():
            self.source = int(self.source)
        self.cap = None

    def connect(self, target_w=1280, target_h=720):
        # Giải phóng kết nối cũ (nếu có)
        self.release()

        # [TỐI ƯU ĐA NỀN TẢNG] BỎ SMART SCAN
        # Chỉ kết nối vào đúng 1 nguồn duy nhất được giao
        return self._try_connect_single(self.source, target_w, target_h)

    def _try_connect_single(self, src, target_w, target_h):
        """Hàm thử kết nối vào 1 source cụ thể"""
        try:
            with _global_cam_lock:
                with FailsafeSuppressStderr():
                    if isinstance(src, int):
                        # [TỐI ƯU ĐA NỀN TẢNG CỐT LÕI]
                        if platform.system() == "Windows":
                            self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
                        else:
                            self.cap = cv2.VideoCapture(src, cv2.CAP_V4L2)
                    else:
                        self.cap = cv2.VideoCapture(src)

            if not self.cap or not self.cap.isOpened():
                return False

            # --- CẤU HÌNH CAMERA ---
            try:
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            except: pass

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_w)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_h)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            # Đọc xả 5 frames liên tục để bật đèn LED và lấy ảnh thực
            success_read = False
            for _ in range(5):
                ret, frame = self.cap.read()
                if ret and frame is not None and frame.any():
                    success_read = True
                    break
                time.sleep(0.1) 

            if not success_read:
                print(f"⚠️ [Cam {self.cam_id}] Không thể lấy được frame hình ảnh từ {src}")
                self.release()
                return False

            print(f"✅ [Cam {self.cam_id}] Đã bắt được hình ảnh thực tế từ nguồn {src}!")
            return True
            
        except Exception as e:
            print(f"⚠️ [Cam {self.cam_id}] Lỗi kết nối: {e}")
            self.release()
            return False

    def read(self):
        if self.cap and self.cap.isOpened():
            return self.cap.read()
        return False, None

    def release(self):
        if self.cap:
            try: self.cap.release()
            except: pass
            self.cap = None