# app/core/oc_enums.py
from enum import Enum

class OrderStatus(str, Enum):
    PACKING = "packing"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class OrderNote(str, Enum):
    # --- START ---
    NEW_ORDER = "Đơn mới hôm nay"
    REPACK = "Đóng lại / Bổ sung (Repack)"
    
    # --- END ---
    TIMEOUT = "Auto-closed: Hết giờ (Timeout)"
    SCAN_NEW = "Auto-closed: Quét mã mới (Scan New)"
    MANUAL = "Manual: Dừng thủ công"
    END_SHIFT = "Auto-closed: Hết ca làm việc (End Shift)"
    
    # --- CANCEL ---
    CHECKING_ONLY = "Auto-cancel: Chỉ kiểm tra hàng (Checking Only)"
    
    # --- SYSTEM ---
    SYSTEM_RESTART = "System: Khởi động lại Server"

# [MỚI] Di chuyển từ packing_machine.py sang đây
class MachineState(Enum):
    IDLE = "IDLE"           # Chờ đơn hàng
    BUFFERING = "BUFFERING" # Đang bầu chọn (Voting)
    PACKING = "PACKING"     # Đang đóng gói

class Action(Enum):
    NONE = 0
    START_ORDER = 1     # Tạo đơn mới
    STOP_ORDER = 2      # Kết thúc đơn
    SNAPSHOT = 3        # Chụp ảnh đại diện
    SWITCH_ORDER = 4    # Đổi đơn nhanh (Gối đầu)