# app/services/google_tts.py
import os
import hashlib
import threading
import platform
import time
from gtts import gTTS
import ctypes

# Thư mục lưu cache âm thanh
CACHE_DIR = "app/media/tts_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

class GoogleTTSService:
    def __init__(self):
        pass

    def _play_mp3(self, file_path):
        """
        Phát file MP3. 
        LƯU Ý: Hàm này sẽ BLOCK (đợi) cho đến khi âm thanh phát xong 
        để đảm bảo không xóa file khi đang phát.
        """
        try:
            if platform.system() == "Linux":
                # [MODIFIED] Linux: Bỏ dấu '&' để đợi phát xong mới return
                os.system(f"mpg123 -q {file_path}")
            
            elif platform.system() == "Windows":
                # Windows: Hàm này đã có lệnh 'wait' nên sẽ tự đợi
                self._play_windows_hidden(file_path)
                
        except Exception as e:
            print(f"❌ [TTS] Play Error: {e}")

    def _play_windows_hidden(self, file_path):
        """
        Sử dụng winmm.dll của Windows để phát nhạc không cần UI.
        """
        try:
            alias = f"tts_{int(time.time()*1000)}"
            # Bọc đường dẫn trong ngoặc kép
            cmd_open = f'open "{file_path}" type mpegvideo alias {alias}'
            # Lệnh 'wait' rất quan trọng: thread sẽ dừng ở đây cho đến khi nói xong
            cmd_play = f'play {alias} wait'
            cmd_close = f'close {alias}'

            ctypes.windll.winmm.mciSendStringW(cmd_open, None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(cmd_play, None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(cmd_close, None, 0, 0)
            
        except Exception as e:
            print(f"⚠️ Windows MCI Error: {e}")
            try:
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
            except: pass

    def speak(self, text, use_cache=True, delete_after_play=True):
        """
        Chuyển văn bản thành giọng nói.
        Args:
            delete_after_play (bool): Xóa file sau khi đọc xong (Mặc định True theo yêu cầu).
        """
        def _worker():
            if not text: return

            # [NEW] 1. Delay 2 giây trước khi bắt đầu xử lý/đọc
            time.sleep(2)

            try:
                # Tạo tên file
                text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
                output_file = os.path.join(CACHE_DIR, f"{text_hash}.mp3")

                # Kiểm tra Cache hoặc tạo mới
                file_ready = False
                if use_cache and os.path.exists(output_file):
                    file_ready = True
                else:
                    # Gọi Google TTS
                    tts = gTTS(text=text, lang='vi')
                    tts.save(output_file)
                    file_ready = True
                
                # Phát file (Hàm này sẽ đợi đến khi nói xong)
                if file_ready:
                    self._play_mp3(output_file)

                # [NEW] 2. Xóa file sau khi đọc xong
                if delete_after_play and os.path.exists(output_file):
                    os.remove(output_file)
                    # print(f"🗑️ [TTS] Deleted: {output_file}") # Uncomment để debug
                
            except Exception as e:
                print(f"❌ [TTS] Generate/Play Error: {e}")

        # Chạy trong luồng riêng
        threading.Thread(target=_worker, daemon=True).start()

# Tạo instance global
tts_service = GoogleTTSService()