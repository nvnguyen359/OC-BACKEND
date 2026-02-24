import uvicorn
import time
import os
import sys
import subprocess

# Thêm đường dẫn để import được service
sys.path.append(os.getcwd())
from app.services.network_service import network_service

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
    time.sleep(5) # Chờ hệ điều hành nhận driver wifi
    
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
            run_setup_mode = True # Cờ báo hiệu phải chạy trang Setup

    # 2. Rẽ nhánh chạy Server tương ứng
    if run_setup_mode:
        print("▶️ Bắt đầu chạy SETUP DASHBOARD Server (Chế độ cấu hình)...")
        # Khởi chạy setup_main.py thay vì main.py
        uvicorn.run("app.setup_main:app", host="0.0.0.0", port=8000, workers=1)
    else:
        print("▶️ Bắt đầu chạy MAIN AI Server (Chế độ giám sát)...")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=1)

if __name__ == "__main__":
    main()