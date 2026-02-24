# app/workers/camera_stream.py
import cv2
import time
import platform
import os
import sys
import threading
import glob

# [QUAN TRỌNG] KHÓA TOÀN CỤC (GLOBAL LOCKS)
_global_cam_lock = threading.Lock()

class FailsafeSuppressStderr:
    """Class giúp ẩn log rác của OpenCV/FFmpeg trên Linux"""
    def __enter__(self):
        try: sys.stderr.flush()
        except: pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class CameraStream:
    def __init__(self, source, cam_id):
        self.source = source
        self.cam_id = cam_id
        # Chuyển đổi sang int nếu là chuỗi số (ví dụ "0" -> 0)
        if isinstance(self.source, str) and self.source.isdigit():
            self.source = int(self.source)
        self.cap = None

    def _find_linux_video_indices(self):
        """
        Hàm dò tìm các cổng video thực tế đang có trên Linux.
        Ví dụ: Tìm thấy /dev/video0, /dev/video1 -> Trả về [0, 1]
        """
        try:
            devs = glob.glob("/dev/video*")
            indices = []
            for d in devs:
                try:
                    # Lọc số từ tên file ("/dev/video1" -> 1)
                    idx = int(d.replace("/dev/video", ""))
                    indices.append(idx)
                except: pass
            return sorted(indices)
        except:
            return []

    def connect(self, target_w=1280, target_h=720):
        # Giải phóng kết nối cũ (nếu có)
        self.release()

        # --- CHIẾN THUẬT: SMART SCAN (DÒ TÌM THÔNG MINH) ---
        # 1. Luôn ưu tiên thử nguồn được cấu hình trước
        candidates = [self.source]
        
        # 2. Nếu là Linux và đang dùng Camera USB (source là số int),
        #    thì quét thêm các cổng khác đề phòng camera bị nhảy cổng.
        if platform.system() == "Linux" and isinstance(self.source, int):
            found_indices = self._find_linux_video_indices()
            for idx in found_indices:
                if idx != self.source:
                    candidates.append(idx)
            
            # [Debug] In ra danh sách sẽ thử nếu có nhiều hơn 1 cổng
            if len(candidates) > 1:
                print(f"🔌 [Cam {self.cam_id}] Smart Scan Candidates: {candidates}")

        # 3. Thử kết nối lần lượt
        for try_src in candidates:
            success = self._try_connect_single(try_src, target_w, target_h)
            if success:
                # Nếu kết nối thành công vào cổng khác cổng gốc -> Cập nhật lại luôn
                if try_src != self.source:
                    print(f"✅ [Cam {self.cam_id}] Auto-switched source: {self.source} -> {try_src}")
                    self.source = try_src 
                return True
        
        return False

    def _try_connect_single(self, src, target_w, target_h):
        """Hàm thử kết nối vào 1 source cụ thể"""
        try:
            with _global_cam_lock:
                with FailsafeSuppressStderr():
                    if isinstance(src, int):
                        if platform.system() == "Windows":
                            self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
                        else:
                            # [FIX QUAN TRỌNG] Linux cần chỉ định CAP_V4L2 để tránh lỗi backend
                            self.cap = cv2.VideoCapture(src, cv2.CAP_V4L2)
                    else:
                        # Trường hợp RTSP hoặc File video
                        self.cap = cv2.VideoCapture(src)

            if not self.cap or not self.cap.isOpened():
                return False

            # --- CẤU HÌNH CAMERA ---
            # 1. Ép dùng MJPEG (Quan trọng cho Orange Pi để giảm tải USB)
            try:
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            except: pass

            # 2. Set độ phân giải
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_w)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_h)
            
            # 3. Giảm buffer để giảm độ trễ (Latency)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # 4. Đọc thử 1 frame để chắc chắn camera hoạt động
            ret, _ = self.cap.read()
            if not ret:
                # Thử lại lần 2 (Đôi khi frame đầu bị đen/lỗi)
                ret, _ = self.cap.read()
                if not ret:
                    self.release()
                    return False
                
            return True
        except Exception:
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