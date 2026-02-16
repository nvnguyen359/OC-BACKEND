import re
# Import instance tts_service từ file bạn đã gửi
from app.services.google_tts import tts_service

class CarrierService:
    def __init__(self):
        # Định nghĩa các đầu mã phổ biến tại Việt Nam
        self.patterns = {
            "Shopee Express": r"^SPXVN\w+",
            "Giao Hàng Tiết Kiệm": r"^S\d+\.\w+",
            "Giao Hàng Nhanh": r"^(GHN|G|K|N)\w+",
            "Viettel Post": r"^VTP\w+",
            "VN Post": r"^[CE]\w+VN$",
            "J&T Express": r"^\d{10,12}$",
            "Ninja Van": r"^(SHP|NLVN)\w+"
        }

    def detect_and_speak(self, tracking_number: str, n_last_chars: int,first_text: str = ""):
        """
        Nhận diện nhà vận chuyển và yêu cầu TTS đọc n ký tự cuối
        """
        tracking_number = str(tracking_number).upper().strip()
        carrier_name = "Không xác định"

        # 1. Nhận diện đơn vị vận chuyển
        for name, pattern in self.patterns.items():
            if re.match(pattern, tracking_number):
                carrier_name = name
                break

        # 2. Lấy n ký tự cuối và tách rời để đọc dễ nghe hơn
        # Ví dụ: '567' -> '5 6 7'
        suffix = tracking_number[-n_last_chars:]
        suffix_spaced = " ".join(list(suffix))

        # 3. Tạo nội dung và gửi vào hàng đợi của GoogleTTS
        content = f"{carrier_name}. {first_text} Mã số {suffix_spaced}"
        
        print(f"📡 [Carrier] Nhận diện: {carrier_name} | Đọc đuôi: {suffix}")
        
        # Gọi hàm speak từ file google_tts.py
        tts_service.speak(content)

# Khởi tạo instance để sử dụng ở các module khác (như Auto Camera)
carrier_service = CarrierService()