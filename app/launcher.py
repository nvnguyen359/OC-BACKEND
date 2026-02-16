# app/launcher.py
import os
import sys
import time
import subprocess
import platform

# -----------------------------------------------------------------------------
# 1. CẤU HÌNH ĐƯỜNG DẪN
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")
SETUP_SCRIPT = os.path.join(BASE_DIR, "setup_main.py")

# Thêm Root Dir vào sys.path để import module
ROOT_DIR = os.path.dirname(BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Import Network Service
try:
    from app.services.network_service import network_service
except ImportError:
    print("⚠️ [Launcher] Critical: Cannot import 'network_service'.")
    network_service = None

# -----------------------------------------------------------------------------
# 2. HÀM HỖ TRỢ
# -----------------------------------------------------------------------------
def run_script(script_path):
    """Chạy script con (main.py hoặc setup_main.py)"""
    print(f"🚀 [LAUNCHER] Executing: {script_path}")
    python_exe = sys.executable
    
    # Kế thừa biến môi trường và PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT_DIR + os.pathsep + env.get("PYTHONPATH", "")

    try:
        subprocess.run([python_exe, script_path], env=env, check=True)
    except KeyboardInterrupt:
        print(f"\n🛑 [LAUNCHER] User stopped {script_path}.")
    except Exception as e:
        print(f"❌ [LAUNCHER] Crash Error: {e}")
        time.sleep(5) # Đợi 5s trước khi thoát để debug nếu cần

# -----------------------------------------------------------------------------
# 3. LOGIC CHÍNH
# -----------------------------------------------------------------------------
def main():
    print("==========================================")
    print("    ORDER CAMERA AI - SYSTEM LAUNCHER     ")
    print("==========================================")
    
    # 1. Windows Mode (Dev)
    if platform.system() == "Windows":
        print("💻 Detected Windows. Skipping network check.")
        run_script(MAIN_SCRIPT)
        return

    # 2. Linux/Orange Pi Mode
    if not network_service:
        print("❌ Error: Network Service not loaded. Exiting.")
        return

    print("🔍 Checking Internet Connection...")
    has_internet = False
    
    # Thử check internet 3 lần (timeout ngắn)
    for i in range(3):
        if network_service.check_internet():
            has_internet = True
            break
        print(f"   Attempt {i+1}/3 failed. Retrying...")
        time.sleep(1.5)

    if has_internet:
        # --- TRƯỜNG HỢP A: CÓ MẠNG ---
        print("✅ Internet ONLINE.")
        
        # Tắt Hotspot nếu nó đang chạy ngầm (để tránh xung đột)
        try:
            network_service.disable_hotspot()
        except: pass
        
        print("🚀 Launching Main Application...")
        run_script(MAIN_SCRIPT)
        
    else:
        # --- TRƯỜNG HỢP B: MẤT MẠNG / KHÔNG KẾT NỐI ĐƯỢC ---
        print("❌ Internet OFFLINE. Entering SETUP MODE...")
        
        # [QUAN TRỌNG] Ngắt kết nối Wifi cũ đang bị treo
        # Nếu không ngắt, wpa_supplicant sẽ chiếm quyền điều khiển wifi, làm hostapd thất bại.
        print("🧹 Cleaning up old connections...")
        try:
            network_service.disconnect_all() 
        except Exception as e:
            print(f"⚠️ Warning during cleanup: {e}")
        
        time.sleep(2) # Đợi 2s để phần cứng ổn định

        # Bật Hotspot
        print("📡 Enabling Hotspot...")
        if network_service.enable_hotspot():
            print("✅ Hotspot Started. Running Setup API...")
            run_script(SETUP_SCRIPT)
        else:
            print("❌ Failed to start Hotspot. System check required.")
            # Vẫn thử chạy setup script phòng trường hợp hotspot đã bật từ trước
            run_script(SETUP_SCRIPT)

if __name__ == "__main__":
    main()