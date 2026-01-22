# app/services/google_tts.py
import os
import hashlib
import threading
import platform
import time
from gtts import gTTS

# [NEW] Import ctypes để gọi hàm hệ thống Windows
import ctypes

# Thư mục lưu cache âm thanh
CACHE_DIR = "app/media/tts_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class GoogleTTSService:
    def __init__(self):
        pass

    def _play_mp3(self, file_path):
        """Phát file MP3 ngầm (Background)"""
        try:
            if platform.system() == "Linux":
                # Linux: Dùng mpg123 chạy nền (-q: quiet, &: background)
                os.system(f"mpg123 -q {file_path} &")
            
            elif platform.system() == "Windows":
                # [FIX] Windows: Dùng MCI (Media Control Interface) để play ngầm hoàn toàn
                self._play_windows_hidden(file_path)
                
        except Exception as e:
            print(f"❌ [TTS] Play Error: {e}")

    def _play_windows_hidden(self, file_path):
        """
        Sử dụng winmm.dll của Windows để phát nhạc không cần UI.
        """
        try:
            # Tạo alias unique để không bị xung đột nếu gọi nhiều lần
            alias = f"tts_{int(time.time()*1000)}"
            
            # Lệnh mở file
            # Lưu ý: Cần bọc đường dẫn trong ngoặc kép để xử lý khoảng trắng
            cmd_open = f'open "{file_path}" type mpegvideo alias {alias}'
            
            # Lệnh phát (thêm 'wait' để thread chờ phát xong mới đóng, 
            # việc này an toàn vì hàm speak đã chạy trong thread riêng)
            cmd_play = f'play {alias} wait'
            
            # Lệnh đóng resource
            cmd_close = f'close {alias}'

            # 1. Mở file
            ctypes.windll.winmm.mciSendStringW(cmd_open, None, 0, 0)
            # 2. Phát file
            ctypes.windll.winmm.mciSendStringW(cmd_play, None, 0, 0)
            # 3. Đóng file (Giải phóng RAM)
            ctypes.windll.winmm.mciSendStringW(cmd_close, None, 0, 0)
            
        except Exception as e:
            print(f"⚠️ Windows MCI Error: {e}")
            # Fallback nếu lỗi: dùng winsound (chỉ hỗ trợ wav, nhưng cứ để đề phòng)
            try:
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
            except: pass

    def speak(self, text, use_cache=True):
        """
        Chuyển văn bản thành giọng nói và phát ngay lập tức.
        Chạy trong Thread riêng để không chặn Camera.
        """
        def _worker():
            if not text: return

            try:
                # 1. Tạo tên file dựa trên nội dung (Cache)
                text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                output_file = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

                # 2. Kiểm tra Cache
                if use_cache and os.path.exists(output_file):
                    self._play_mp3(output_file)
                    return

                # 3. Gọi Google TTS
                tts = gTTS(text=text, lang='vi')
                tts.save(output_file)
                
                # 4. Phát file
                self._play_mp3(output_file)
                
            except Exception as e:
                print(f"❌ [TTS] Generate Error: {e}")

        # Fire and Forget
        threading.Thread(target=_worker, daemon=True).start()

# Tạo instance global
tts_service = GoogleTTSService()