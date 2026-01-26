# app/workers/camera_stream.py
import cv2
import time
import platform
import os
import sys
import threading

# [QUAN TRỌNG] KHÓA TOÀN CỤC (GLOBAL LOCKS)
_global_cam_lock = threading.Lock()
_stderr_lock = threading.Lock()

# [FIX] Class chặn log "An toàn": Loại bỏ os.dup2 để tránh lỗi WinError 5
class FailsafeSuppressStderr:
    def __enter__(self):
        # Chỉ cần flush để đẩy hết log cũ đi, không can thiệp vào File Descriptor
        try: sys.stderr.flush()
        except: pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class CameraStream:
    def __init__(self, source, cam_id):
        self.source = source
        self.cam_id = cam_id
        if isinstance(self.source, str) and self.source.isdigit():
            self.source = int(self.source)
        self.cap = None

    def connect(self, target_w=1280, target_h=720):
        self.release()
        try:
            # [FIX] DÙNG KHÓA TOÀN CỤC
            with _global_cam_lock:
                # Dù class này giờ "vô hại", vẫn giữ context manager để code gọn gàng
                with FailsafeSuppressStderr():
                    if isinstance(self.source, int) and platform.system() == "Windows":
                        self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
                    else:
                        self.cap = cv2.VideoCapture(self.source)

            if not self.cap or not self.cap.isOpened():
                return False

            # [FIX QUAN TRỌNG] Tôn trọng cấu hình độ phân giải (Hỗ trợ 2K/4K)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_w)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_h)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Đọc thử 1 frame
            ret, _ = self.cap.read()
            if not ret:
                self.release()
                return False
                
            return True
        except:
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