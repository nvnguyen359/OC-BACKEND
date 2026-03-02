# app/workers/video_recorder.py
import time
import os
import threading
import queue
from app.services.media_service import media_service

class VideoRecorder:
    def __init__(self, fps=20.0):
        self.writer = None
        self.file_path = None
        self.start_time = 0
        self.written_frames = 0
        self.fps = fps
        
        # [FIX NGUYÊN NHÂN 3] Hàng đợi và luồng ghi ngầm chống lag SD Card
        self.frame_queue = queue.Queue(maxsize=30) 
        self.is_recording = False
        self.record_thread = None

    def start(self, code, width, height):
        try:
            self.writer, self.file_path = media_service.create_video_writer(
                code, width, height, self.fps
            )
            self.start_time = time.time()
            self.written_frames = 0
            
            self.is_recording = True
            while not self.frame_queue.empty():
                try: self.frame_queue.get_nowait()
                except: pass
            
            self.record_thread = threading.Thread(target=self._record_loop, daemon=True)
            self.record_thread.start()
            return True
        except Exception as e:
            print(f"❌ Recorder Start Error: {e}")
            return False

    def _record_loop(self):
        """Luồng chuyên biệt để ghi thẻ nhớ, tách biệt với việc đọc camera"""
        while self.is_recording or not self.frame_queue.empty():
            try:
                frame = self.frame_queue.get(timeout=0.1)
                if self.writer:
                    self.writer.write(frame)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Record Loop Error: {e}")

    def write_frame(self, frame):
        """Đẩy thẳng vào hàng đợi (Queue), không bắt camera phải chờ ghi thẻ nhớ"""
        if self.is_recording and self.writer:
            elapsed = time.time() - self.start_time
            expected_frames = int(elapsed * self.fps)
            frames_to_add = expected_frames - self.written_frames
            
            if frames_to_add > 0:
                count = min(frames_to_add, 5)
                for _ in range(count):
                    try:
                        self.frame_queue.put_nowait(frame.copy())
                        self.written_frames += 1
                    except queue.Full:
                        # Thẻ nhớ bị tắc nghẽn -> Vứt bớt frame chứ không kéo lag toàn hệ thống
                        break

    def stop(self):
        self.is_recording = False
        if self.record_thread:
            self.record_thread.join(timeout=2.0)
            
        path = self.file_path
        if self.writer:
            self.writer.release()
            self.writer = None
        return path

    def snapshot(self, frame, code):
        if frame is None: return None
        return media_service.save_snapshot(frame, code)