# app/launcher.py
import sys
import os
from pathlib import Path

# [FIX PATH] Định vị tuyệt đối thư mục gốc của dự án (OC-BACkEND)
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import uvicorn
import time
import subprocess
import signal

from app.services.network_service import network_service

# =========================================================================
# [FIX CỰC MẠNH] HÀM ÉP TẮT HỆ THỐNG NGAY LẬP TỨC
# =========================================================================
def force_quit_handler(signum, frame):
    print("\n🛑 [BÁO ĐỘNG] Nhận lệnh tắt bằng Ctrl+C! Đang dọn dẹp hệ thống...")
    try:
        from app.workers.run_worker import stop_all_workers
        stop_all_workers()
    except Exception as e:
        print(f"⚠️ Lỗi dọn dẹp: {e}")
    print("⚡ [HỆ THỐNG] Dọn dẹp xong. Rút điện an toàn!")
    os._exit(0)

signal.signal(signal.SIGINT, force_quit_handler)
if sys.platform != "win32":
    signal.signal(signal.SIGTERM, force_quit_handler)

class CustomUvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

def get_current_ip():
    """Lấy IP hiện tại của wlan0"""
    try:
        output = subprocess.check_output("ip -4 addr show wlan0", shell=True).decode()
        for line in output.split('\n'):
            if "inet " in line:
                return line.split()[1].split('/')[0]
    except:
        pass
    return ""

def main():
    print("🚀 [LAUNCHER] Hệ thống đang khởi động...")
    time.sleep(5) 
    
    run_setup_mode = False
    
    # 1. Kiểm tra mạng
    if network_service.check_internet():
        print("✅ Đã có Internet. Chạy chế độ AI Camera bình thường.")
    else:
        print("⚠️ Không có Internet. Đang kiểm tra IP Wifi...")
        ip_check = get_current_ip()
        
        if ip_check and ip_check != "192.168.42.1" and not ip_check.startswith("169.254"):
             print(f"✅ Đã kết nối Wifi nội bộ (IP: {ip_check}). Không cần Hotspot.")
        else:
            print("❌ Mất kết nối hoàn toàn. KÍCH HOẠT HOTSPOT FALLBACK...")
            network_service.enable_hotspot()
            run_setup_mode = True 

    # 2. Khởi tạo cấu hình Server
    if run_setup_mode:
        print("▶️ Bắt đầu chạy SETUP DASHBOARD Server (Chế độ cấu hình)...")
        config = uvicorn.Config("app.setup_main:app", host="0.0.0.0", port=8000, workers=1)
    else:
        print("▶️ Bắt đầu chạy MAIN AI Server (Chế độ giám sát)...")
        config = uvicorn.Config("app.main:app", host="0.0.0.0", port=8000, workers=1)
        
    server = CustomUvicornServer(config)
    server.run()

if __name__ == "__main__":
    main()