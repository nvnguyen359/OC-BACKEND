import os
import hashlib
import threading
import platform
import time
import queue
import subprocess
import ctypes
from gtts import gTTS

# Cấu hình thư mục
CACHE_DIR = "app/media/tts_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class GoogleTTSService:
    def __init__(self):
        # Hàng đợi chứa các câu cần đọc
        self.queue = queue.Queue()
        self.is_running = True
        self.os_type = platform.system()
        
        # Khởi tạo luồng xử lý duy nhất (Worker)
        # daemon=True để luồng tự tắt khi chương trình chính tắt
        self.worker_thread = threading.Thread(target=self._worker_process, daemon=True, name="TTS_Worker")
        self.worker_thread.start()

        print(f"🔈 [TTS] Service Started on {self.os_type}")

    def speak(self, text, priority=False):
        """
        Thêm yêu cầu đọc vào hàng đợi.
        Args:
            text (str): Nội dung cần đọc.
            priority (bool): (Mở rộng) Sau này có thể dùng để chèn thông báo khẩn cấp.
        """
        if not text: return
        # Đẩy vào queue, worker sẽ tự lấy ra xử lý
        self.queue.put(text)

    def _worker_process(self):
        """
        Luồng chạy ngầm liên tục để xử lý hàng đợi.
        Đảm bảo chỉ có 1 tiến trình phát âm thanh tại 1 thời điểm.
        """
        while self.is_running:
            try:
                # Lấy text từ queue, chờ tối đa 1s nếu rỗng
                text = self.queue.get(timeout=1.0)
                
                # Xử lý đọc
                self._process_speech(text)
                
                # Báo hiệu đã xử lý xong item này
                self.queue.task_done()
                
                # Nghỉ nhẹ giữa các câu để âm thanh tách bạch
                time.sleep(0.5) 
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ [TTS Worker Error] {e}")

    def _process_speech(self, text):
        try:
            # 1. Tạo đường dẫn file (Hash để tránh trùng tên file lỗi)
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            file_path = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

            # 2. Gọi Google API nếu file chưa có
            if not os.path.exists(file_path):
                tts = gTTS(text=text, lang='vi')
                tts.save(file_path)

            # 3. Phát âm thanh theo hệ điều hành
            if self.os_type == "Linux":
                self._play_linux(file_path)
            elif self.os_type == "Windows":
                self._play_windows(file_path)

            # 4. Xóa file ngay sau khi đọc (Tiết kiệm bộ nhớ cho Pi)
            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            print(f"⚠️ [TTS Fail] '{text}': {e}")

    def _play_linux(self, file_path):
        """
        Phát trên Orange Pi/Linux tối ưu với mpg123
        """
        try:
            # Cấu hình tối ưu cho OP3:
            # -o pulse: Dùng PulseAudio (Fix lỗi Deep trouble flush)
            # --buffer 1024: Tăng bộ nhớ đệm để không bị vấp khi CPU cao
            # -q: Im lặng (không in log ra terminal)
            cmd = ["mpg123", "-o", "pulse", "--buffer", "1024", "-q", file_path]
            
            # Fallback: Nếu không có Pulse, thử chạy ALSA mặc định
            # Kiểm tra xem pulseaudio có đang chạy không
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                # Nếu lệnh trên lỗi, thử chạy mode basic
                os.system(f"mpg123 -q {file_path}")
                
        except Exception as e:
            print(f"Linux Audio Err: {e}")

    def _play_windows(self, file_path):
        """
        Phát trên Windows dùng winmm.dll (Giữ nguyên logic cũ của bạn vì nó ổn)
        """
        try:
            alias = f"tts_{int(time.time()*1000)}"
            cmd_open = f'open "{file_path}" type mpegvideo alias {alias}'
            cmd_play = f'play {alias} wait' # Wait để block thread cho đến khi xong
            cmd_close = f'close {alias}'

            ctypes.windll.winmm.mciSendStringW(cmd_open, None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(cmd_play, None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(cmd_close, None, 0, 0)
        except:
            # Fallback đơn giản
            try:
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
            except: pass

# Tạo instance global để các file khác import dùng luôn
tts_service = GoogleTTSService()