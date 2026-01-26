# app/launcher.py
import os
import sys
import time
import subprocess
import platform

# -----------------------------------------------------------------------------
# 1. CẤU HÌNH ĐƯỜNG DẪN ĐỘNG (AUTO-PATH)
# -----------------------------------------------------------------------------
# Lấy thư mục chứa file launcher.py này (tức là thư mục 'app/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Định nghĩa đường dẫn tuyệt đối đến các file anh em
MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")
SETUP_SCRIPT = os.path.join(BASE_DIR, "setup_main.py")

# Thử import network service
# Vì launcher nằm trong 'app/', ta cần thêm thư mục cha (Root) vào sys.path để import được 'app.*'
ROOT_DIR = os.path.dirname(BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from app.services.network_service import network_service
except ImportError:
    # Fallback chỉ để không crash ngay lập tức nếu môi trường chưa chuẩn
    print("⚠️ [Launcher] Warning: Cannot import 'network_service'. Check PYTHONPATH.")
    network_service = None

# -----------------------------------------------------------------------------
# 2. HÀM CHẠY SCRIPT
# -----------------------------------------------------------------------------
def run_script(script_path):
    """
    Hàm wrapper để gọi python script con với môi trường chuẩn.
    """
    print(f"🚀 [LAUNCHER] Executing: {script_path}")
    
    # Lấy đường dẫn python hiện tại (đang chạy trong venv)
    python_exe = sys.executable
    
    # Chuẩn bị biến môi trường: Thêm ROOT_DIR vào PYTHONPATH cho tiến trình con
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT_DIR + os.pathsep + env.get("PYTHONPATH", "")

    try:
        # Gọi subprocess
        subprocess.run([python_exe, script_path], env=env, check=True)
    except KeyboardInterrupt:
        print(f"\n🛑 [LAUNCHER] User stopped {script_path}.")
    except Exception as e:
        print(f"❌ [LAUNCHER] Crash Error: {e}")
        time.sleep(5)

# -----------------------------------------------------------------------------
# 3. LOGIC CHÍNH
# -----------------------------------------------------------------------------
def main():
    print("==========================================")
    print("    ORDER CAMERA AI - SYSTEM LAUNCHER     ")
    print("==========================================")
    print(f"📂 Working Directory: {os.getcwd()}")
    print(f"📂 Launcher Location: {BASE_DIR}")
    
    # 1. Phát hiện hệ điều hành
    is_windows = platform.system() == "Windows"

    # [WINDOWS] Chạy thẳng vào App chính
    if is_windows:
        print("💻 Detected Windows. Skipping network check.")
        run_script(MAIN_SCRIPT)
        return

    # [LINUX/ORANGE PI] Logic kiểm tra mạng
    if not network_service:
        print("❌ Error: Network Service not loaded. Exiting.")
        return

    print("🔍 Checking Internet Connection...")
    has_internet = False
    for i in range(3):
        if network_service.check_internet():
            has_internet = True
            break
        print(f"   Attempt {i+1}/3 failed. Retrying in 2s...")
        time.sleep(2)

    if has_internet:
        # --- TRƯỜNG HỢP A: CÓ MẠNG ---
        print("✅ Internet ONLINE. Launching Main Application...")
        run_script(MAIN_SCRIPT)
    else:
        # --- TRƯỜNG HỢP B: MẤT MẠNG ---
        print("❌ Internet OFFLINE. Entering SETUP MODE...")
        
        # 1. Bật Hotspot
        network_service.enable_hotspot()
        
        # 2. Chạy Mini-API Setup
        print("🛠 Starting Setup API...")
        run_script(SETUP_SCRIPT)

if __name__ == "__main__":
    main()