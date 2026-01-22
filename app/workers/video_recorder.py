# Quản lý logic ghi hình, đảm bảo đúng FPS thực tế, gọi service lưu file.
import time
import os
from app.services.media_service import media_service

class VideoRecorder:
    def __init__(self, fps=20.0):
        self.writer = None
        self.file_path = None
        self.start_time = 0
        self.written_frames = 0
        self.fps = fps

    def start(self, code, width, height):
        """Khởi tạo Video Writer thông qua Media Service"""
        try:
            self.writer, self.file_path = media_service.create_video_writer(
                code, width, height, self.fps
            )
            self.start_time = time.time()
            self.written_frames = 0
            return True
        except Exception as e:
            print(f"❌ Recorder Start Error: {e}")
            return False

    def write_frame(self, frame):
        """Ghi frame có đồng bộ thời gian thực"""
        if self.writer:
            elapsed = time.time() - self.start_time
            expected_frames = int(elapsed * self.fps)
            frames_to_add = expected_frames - self.written_frames
            
            # Chỉ ghi bù tối đa 5 frame để tránh lag
            if frames_to_add > 0:
                count = min(frames_to_add, 5)
                for _ in range(count):
                    self.writer.write(frame)
                    self.written_frames += 1

    def stop(self):
        if self.writer:
            self.writer.release()
            self.writer = None
        return self.file_path

    def snapshot(self, frame, code):
        """Lưu ảnh snapshot"""
        if frame is None: return None
        return media_service.save_snapshot(frame, code)