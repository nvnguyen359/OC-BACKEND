# app/workers/run_worker.py
import os
import time
import multiprocessing
import platform
import threading
import signal

os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"
os.environ["OPENCV_LOG_LEVEL"] = "SILENT" 
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_OBSENSOR"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

def start_all_workers():
    from app.workers.camera_worker import camera_system
    from app.workers.disk_manager_worker import disk_manager_worker
    from app.services.upload_service import upload_service 
    
    try:
        from app.workers.upsert_camera_worker import upsert_camera_worker
    except ModuleNotFoundError:
        upsert_camera_worker = None

    print("============== STARTING WORKERS ==============")
    camera_system.start()
    if camera_system.is_system_running:
        print("✅ [RunWorker] Camera System is RUNNING.")

    if upsert_camera_worker:
        upsert_camera_worker.start()
    
    disk_manager_worker.start()
    print("================ WORKERS STARTED =============")
    return camera_system, disk_manager_worker, upsert_camera_worker

def force_kill_after_timeout(timeout=5):
    """Luồng Sát thủ: Đếm ngược thời gian, quá hạn là dùng lệnh Hệ Điều Hành chém chết tiến trình!"""
    time.sleep(timeout)
    print(f"\n⚡ [CẢNH BÁO] Máy chủ Uvicorn bị kẹt quá {timeout}s. Ép thoát bằng SIGKILL!!!")
    try:
        # Lệnh tuyệt đối của Linux/Windows, giết tiến trình ngay tắp lự
        os.kill(os.getpid(), signal.SIGKILL)
    except:
        os._exit(0)

def stop_all_workers(cam_sys, disk_sys, up_sys):
    print("\n============== STOPPING WORKERS ==============")
    
    # [FIX QUAN TRỌNG NHẤT]: Bật sát thủ ngay khi FastAPI gọi tắt ứng dụng
    threading.Thread(target=force_kill_after_timeout, args=(5,), daemon=True).start()
    
    try:
        if up_sys: up_sys.stop()
        if disk_sys: disk_sys.stop()
        if cam_sys: cam_sys.shutdown()
    except Exception as e: 
        print(f"Error stopping workers: {e}")
    print("================ WORKERS STOPPED =============")

def auto_reboot_worker(cam_sys, disk_sys, up_sys):
    import pytz
    from datetime import datetime
    print("🔄 [System] Luồng Auto-Reboot đã kích hoạt (Lịch trình bảo trì: 03:00 AM)...")
    
    while True:
        time.sleep(30)
        try:
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(tz)
            
            if now.hour == 3 and now.minute == 0:
                print("\n" + "="*55)
                print("⏰ [AUTO-REBOOT] Đã đến giờ bảo trì định kỳ (03:00 AM)!")
                print("⏰ [AUTO-REBOOT] Đang dọn dẹp dữ liệu để khởi động lại mạch...")
                print("="*55 + "\n")
                
                threading.Thread(target=lambda: (time.sleep(15), os.system("sudo reboot")), daemon=True).start()
                stop_all_workers(cam_sys, disk_sys, up_sys)
                print("🚀 [AUTO-REBOOT] Ra lệnh REBOOT tới hệ điều hành...")
                time.sleep(2)
                os.system("sudo reboot")
                time.sleep(120) 
        except Exception as e:
            pass

if __name__ == "__main__":
    multiprocessing.freeze_support()
    try: 
        multiprocessing.set_start_method('spawn', force=True)
    except: pass
        
    cam_sys, disk_sys, up_sys = start_all_workers()
    
    threading.Thread(
        target=auto_reboot_worker, 
        args=(cam_sys, disk_sys, up_sys), 
        daemon=True, 
        name="AutoReboot"
    ).start()
    
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n⚡ Nhận lệnh tắt (Ctrl+C). Đang xử lý dừng khẩn cấp...")
        stop_all_workers(cam_sys, disk_sys, up_sys)