# app/workers/camera_system.py
import sys
import threading
import time
import multiprocessing
import signal
import psutil
import os
import platform
import subprocess
from typing import Dict

# --- IMPORTS ---
from app.workers.ai_detector import run_ai_process
from app.db.session import SessionLocal
from app.workers.camera_runtime import CameraRuntime
from app.services.socket_service import socket_service

class CameraSystem:
    def __init__(self):
        self.cameras: Dict[int, CameraRuntime] = {}
        self.ai_input = multiprocessing.Queue(maxsize=10)
        self.ai_output = multiprocessing.Queue()
        self.os_type = platform.system()
        
        self.system_stats = {
            "cpu_overall": 0.0,
            "ram_percent": 0.0,
            "ram_used_mb": 0.0,
            "temp_c": 0.0,
            "disk_percent": 0.0,
            "disk_free_gb": 0.0,
            "threads": 0,
            "active_cams": 0,
            "uptime": 0
        }
        
        self.ai_process = None
        self.is_system_running = False
        self.start_time = time.time()

    def start(self):
        if self.is_system_running: return
        self.is_system_running = True
        print(f"🚀 [System] Camera Core started on {self.os_type}")

        self.ai_process = multiprocessing.Process(
            target=run_ai_process, 
            args=(self.ai_input, self.ai_output, "yolov8n.pt"), 
            daemon=True
        )
        self.ai_process.start()
        
        try: 
            signal.signal(signal.SIGINT, lambda s, f: (self.shutdown(), sys.exit(0)))
        except (ValueError, AttributeError): pass
        
        threading.Thread(target=self._listen_ai, daemon=True, name="AI_Listener").start()
        threading.Thread(target=self._monitor_resources, daemon=True, name="Res_Monitor").start()
        threading.Thread(target=self._startup_load_cameras, daemon=True, name="DB_Loader").start()

    def _get_temperature(self):
        """Hàm lấy nhiệt độ đa nền tảng - Fix lỗi N/A trên Windows"""
        temp = 0.0
        
        if self.os_type == "Linux":
            # Ưu tiên psutil trên Linux (Orange Pi)
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    for label in ['cpu_thermal', 'soc_thermal', 'thermal_zone0', 'cpu-thermal', 'coretemp']:
                        if label in temps and temps[label]:
                            return round(temps[label][0].current, 1)
                # Fallback đọc file hệ thống
                for i in range(3):
                    path = f"/sys/class/thermal/thermal_zone{i}/temp"
                    if os.path.exists(path):
                        with open(path, "r") as f:
                            return round(int(f.read().strip()) / 1000.0, 1)
            except: pass

        elif self.os_type == "Windows":
            # Thử lấy nhiệt độ qua WMIC (Windows Management Instrumentation)
            try:
                # Lệnh này yêu cầu chạy PowerShell/CMD với quyền Admin để trả về số liệu chính xác
                cmd = "wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature"
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    raw_temp = float(lines[1].strip())
                    # Công thức: (Độ Kelvin * 10 - 2732) / 10 = Độ C
                    c_temp = (raw_temp - 2732) / 10.0
                    if 10 < c_temp < 110: # Lọc các giá trị vô lý
                        return round(c_temp, 1)
            except:
                pass
            
            # Nếu WMIC không được, thử psutil (hiếm khi có trên Windows trừ khi có driver đặc biệt)
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    if temps:
                        return round(list(temps.values())[0][0].current, 1)
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
                
                # Gọi hàm lấy nhiệt độ mới hỗ trợ Windows
                current_temp = self._get_temperature()

                self.system_stats.update({
                    "cpu_overall": cpu_p,
                    "ram_percent": ram.percent,
                    "ram_used_mb": round(ram.used / (1024 * 1024), 1),
                    "temp_c": current_temp,
                    "disk_percent": disk.percent,
                    "disk_free_gb": round(disk.free / (1024**3), 1),
                    "threads": threading.active_count(),
                    "active_cams": sum(1 for c in self.cameras.values() if c.is_connected),
                    "uptime": int(time.time() - self.start_time)
                })

                socket_service.broadcast_event("SYSTEM_STATS", self.system_stats)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ [Monitor Error] {e}")
                time.sleep(5)

    def _listen_ai(self):
        while self.is_system_running:
            try:
                result = self.ai_output.get(timeout=0.5)
                if result.get('cam_id') in self.cameras:
                    self.cameras[result['cam_id']].ai_metadata = result.get('data', [])
            except: pass

    # --- [ADDED] Method fix lỗi Hot-reload trigger failed ---
    def reload_settings(self):
        """
        Được gọi khi người dùng lưu cài đặt.
        Duyệt qua các camera đang chạy và yêu cầu tải lại config.
        """
        print("🔄 [System] Hot-reloading settings for all cameras...")
        for cid, cam in self.cameras.items():
            if cam.is_running:
                try:
                    # Gọi hàm load setting nội bộ của CameraRuntime
                    if hasattr(cam, '_load_and_apply_settings'):
                        cam._load_and_apply_settings()
                        
                    # Cập nhật lại FPS cho recorder (vì recorder object cần set lại thuộc tính)
                    if hasattr(cam, 'recorder') and hasattr(cam, 'fps_record'):
                        cam.recorder.fps = cam.fps_record
                        
                    print(f"✅ [Cam {cid}] Settings reloaded.")
                except Exception as e:
                    print(f"⚠️ [Cam {cid}] Hot-reload failed: {e}")

    def shutdown(self):
        self.is_system_running = False
        for cid in list(self.cameras.keys()):
            try: self.cameras[cid].stop()
            except: pass
        if self.ai_process and self.ai_process.is_alive(): 
            self.ai_process.terminate()
        print("✅ [System] Shutdown complete.")

    def add_camera(self, cid, src):
        if cid in self.cameras: self.stop_camera(cid)
        self.cameras[cid] = CameraRuntime(cid, src, self.ai_input)
    
    def stop_camera(self, cid):
        if cid in self.cameras:
            try: self.cameras[cid].stop()
            except: pass
            del self.cameras[cid]

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