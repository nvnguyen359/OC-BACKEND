# app/workers/camera_system.py
import sys
import threading
import time
import multiprocessing
import psutil
import os
import platform
import subprocess
import signal
from typing import Dict

# --- IMPORTS ---
from app.workers.ai_detector import run_ai_process
from app.db.session import SessionLocal
from app.workers.camera_runtime import CameraRuntime
from app.services.socket_service import socket_service

class CameraSystem:
    def __init__(self):
        self.cameras: Dict[int, CameraRuntime] = {}
        
        self.manager = None
        self.ai_input = None
        self.ai_output = None
        
        self.os_type = platform.system()
        
        self.system_stats = {
            "cpu_overall": 0.0, "ram_percent": 0.0, "ram_used_mb": 0.0,
            "temp_c": 0.0, "disk_percent": 0.0, "disk_free_gb": 0.0,
            "threads": 0, "active_cams": 0, "uptime": 0
        }
        
        self.ai_process = None
        self.is_system_running = False
        self.start_time = time.time()

    def start(self):
        if self.is_system_running: return
        self.is_system_running = True
        
        if self.os_type == "Windows":
            print(f"🚀 [System] Camera Core started on {self.os_type} (Safe Manager Mode)")
            self.manager = multiprocessing.Manager()
            self.ai_input = self.manager.Queue(maxsize=10)
            self.ai_output = self.manager.Queue()
        else:
            print(f"🚀 [System] Camera Core started on Linux/OPi3 (Native Fast Queue)")
            self.manager = None
            self.ai_input = multiprocessing.Queue(maxsize=10)
            self.ai_output = multiprocessing.Queue()

        self.ai_process = multiprocessing.Process(
            target=run_ai_process, 
            args=(self.ai_input, self.ai_output, "yolov8n.pt"), 
            daemon=True
        )
        self.ai_process.start()
        
        threading.Thread(target=self._listen_ai, daemon=True, name="AI_Listener").start()
        threading.Thread(target=self._monitor_resources, daemon=True, name="Res_Monitor").start()
        threading.Thread(target=self._startup_load_cameras, daemon=True, name="DB_Loader").start()

    def _get_temperature(self):
        temp = 0.0
        if self.os_type == "Linux":
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    for label in ['cpu_thermal', 'soc_thermal', 'thermal_zone0', 'cpu-thermal', 'coretemp']:
                        if label in temps and temps[label]:
                            return round(temps[label][0].current, 1)
                for i in range(3):
                    path = f"/sys/class/thermal/thermal_zone{i}/temp"
                    if os.path.exists(path):
                        with open(path, "r") as f:
                            return round(int(f.read().strip()) / 1000.0, 1)
            except: pass
        elif self.os_type == "Windows":
            try:
                cmd = "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature"
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    raw_temp = float(lines[1].strip())
                    c_temp = (raw_temp - 2732) / 10.0
                    if 10 < c_temp < 110: return round(c_temp, 1)
            except: pass
        return temp

    def _monitor_resources(self):
        print("📊 [System] Resource Monitor Started.")
        while self.is_system_running:
            try:
                cpu_p = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory()
                disk_path = 'C:\\' if self.os_type == "Windows" else '/'
                disk = psutil.disk_usage(disk_path)

                self.system_stats.update({
                    "cpu_overall": cpu_p, "ram_percent": ram.percent,
                    "ram_used_mb": round(ram.used / (1024 * 1024), 1),
                    "temp_c": self._get_temperature(), "disk_percent": disk.percent,
                    "disk_free_gb": round(disk.free / (1024**3), 1),
                    "threads": threading.active_count(),
                    "active_cams": sum(1 for c in self.cameras.values() if getattr(c, 'is_connected', False)),
                    "uptime": int(time.time() - self.start_time)
                })

                socket_service.broadcast_event("SYSTEM_STATS", self.system_stats)
                time.sleep(2)
            except: time.sleep(5)

    def _listen_ai(self):
        while self.is_system_running:
            try:
                if self.ai_output:
                    try:
                        result = self.ai_output.get(timeout=0.1)
                        if result and result.get('cam_id') in self.cameras:
                            self.cameras[result['cam_id']].ai_metadata = result.get('data', [])
                    except: pass
            except: pass

    def reload_settings(self):
        for cam in list(self.cameras.values()):
            if cam.is_running:
                try:
                    if hasattr(cam, '_load_and_apply_settings'):
                        cam._load_and_apply_settings()
                    if hasattr(cam, 'recorder') and hasattr(cam, 'fps_record'):
                        cam.recorder.fps = cam.fps_record
                except: pass

    def shutdown(self):
        print("🛑 [System] Bắt đầu tiến trình tắt hệ thống...")
        self.is_system_running = False
        
        # 1. DIỆT TẬN GỐC TIẾN TRÌNH AI
        # Bắn bỏ ngay lập tức để ngắt quyền truy cập vào Queue, chặn đứt Deadlock
        if self.ai_process:
            print("🛑 [System] Ép diệt AI Process để giải phóng tài nguyên...")
            try:
                if self.ai_process.pid:
                    if platform.system() == "Windows":
                        os.kill(self.ai_process.pid, signal.SIGTERM)
                    else:
                        os.kill(self.ai_process.pid, signal.SIGKILL)
            except: pass
            
        time.sleep(0.2) # Cho OS thời gian dọn rác

        # 2. Đóng Camera và lưu file Video
        for cam in list(self.cameras.values()):
            try: 
                print(f"🛑 [System] Đang đóng gói dữ liệu Camera {getattr(cam, 'cam_id', '?')}...")
                cam.is_running = False
                cam.stop()
            except Exception as e: 
                print(f"⚠️ Lỗi tắt cam: {e}")

        # 3. Cắt đứt các liên kết còn lại
        self.manager = None
        self.ai_input = None
        self.ai_output = None
        print("✅ [System] Giải phóng hoàn tất! Có thể thoát an toàn.")

    def add_camera(self, cid, src):
        self.stop_camera(cid)
        self.cameras[cid] = CameraRuntime(cid, src, self.ai_input)
    
    def stop_camera(self, cid):
        cam = self.cameras.pop(cid, None)
        if cam:
            try: cam.stop()
            except Exception as e: print(f"⚠️ [System] Lỗi khi stop luồng camera {cid}: {e}")

    def _startup_load_cameras(self):
        time.sleep(2)
        db = SessionLocal()
        try:
            from app.crud.camera_crud import camera_crud
            for cam in camera_crud.get_all(db):
                if getattr(cam, 'status', 'OFF') == 'ACTIVE':
                    src = cam.rtsp_url if (cam.rtsp_url and len(cam.rtsp_url) > 5) else cam.os_index
                    if src is not None: self.add_camera(cam.id, src)
        finally: db.close()

camera_system = CameraSystem()