import cv2
import time
import platform
import os
import sys

# Helper chặn log rác
# Quản lý kết nối Camera, tự động reconnect, cài đặt độ phân giải tối ưu cho Orange Pi.
class FailsafeSuppressStderr:
    def __enter__(self):
        try:
            sys.stderr.flush()
            self.devnull = os.open(os.devnull, os.O_RDWR)
            self.saved_stderr = os.dup(sys.stderr.fileno())
            os.dup2(self.devnull, sys.stderr.fileno())
        except: pass
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            os.dup2(self.saved_stderr, sys.stderr.fileno())
            os.close(self.devnull)
        except: pass

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
            with FailsafeSuppressStderr():
                if isinstance(self.source, int) and platform.system() == "Windows":
                    self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
                else:
                    self.cap = cv2.VideoCapture(self.source)

            if not self.cap or not self.cap.isOpened():
                return False

            # [TỐI ƯU] Luôn set HD 720p để nhẹ cho Orange Pi 3
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return True
        except:
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