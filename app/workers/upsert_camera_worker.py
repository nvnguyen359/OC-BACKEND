# app/workers/upsert_camera_worker.py
import os
import threading
import time
import platform
import sys
import traceback

# TẮT LOG RÁC CỦA OPENCV
os.environ["OPENCV_LOG_LEVEL"] = "OFF"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_OBSENSOR"] = "0"

try: 
    import cv2
except ImportError: 
    cv2 = None

try:
    from app.db.session import SessionLocal 
    from app.crud.camera_crud import camera_crud
    from app.db import schemas
    from app.workers.camera_worker import camera_system
    from app.workers.camera_stream import FailsafeSuppressStderr, _global_cam_lock
except ImportError:
    SessionLocal = None; camera_crud = None; schemas = None; camera_system = None
    FailsafeSuppressStderr = None; _global_cam_lock = None

def is_index_actively_used_and_connected(idx: int) -> bool:
    if not camera_system: return False
    for cam_runner in camera_system.cameras.values():
        if getattr(cam_runner, 'is_running', False) and getattr(cam_runner, 'is_connected', False):
            try:
                src = getattr(cam_runner.stream, 'source', None)
                if str(src) == str(idx): 
                    return True
            except: continue
    return False

def check_physical_device(os_index: int) -> bool:
    if platform.system() == "Linux" and not os.path.exists(f"/dev/video{os_index}"):
        return False
    if is_index_actively_used_and_connected(os_index):
        return True
    if cv2 is None: return False
    is_opened = False
    cap = None
    try:
        backend = cv2.CAP_DSHOW if platform.system() == 'Windows' else cv2.CAP_V4L2
        lock_acquired = False
        if _global_cam_lock:
            lock_acquired = _global_cam_lock.acquire(timeout=2.0)
        try:
            if lock_acquired or (_global_cam_lock is None):
                if FailsafeSuppressStderr:
                    with FailsafeSuppressStderr(): cap = cv2.VideoCapture(os_index, backend)
                else: cap = cv2.VideoCapture(os_index, backend)
                
                if cap and cap.isOpened():
                    ret, _ = cap.read()
                    if ret: is_opened = True
        finally:
            if cap: cap.release()
            if lock_acquired and _global_cam_lock: _global_cam_lock.release()
            time.sleep(0.1)
    except: pass
    return is_opened

class UpsertCameraWorker:
    def __init__(self, interval=5, max_scan_index=4):
        self.interval = interval
        self.max_scan_index = max_scan_index
        self.is_running = False
        self.thread = None
        self.pending_new_cam_cycles = {} 

    def start(self):
        if self.is_running: return
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"🛡️ [UpsertWorker] Auto-Discovery Started (Index 0-{self.max_scan_index})...")

    def stop(self):
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

    def _run_loop(self):
        while self.is_running:
            if not SessionLocal or not camera_crud:
                time.sleep(self.interval)
                continue

            db = None
            try:
                db = SessionLocal()
                db_cameras = camera_crud.get_all(db)
                
                for cam in db_cameras:
                    if cam.status == 'OFF' and camera_system and cam.id in camera_system.cameras:
                        self._sync_system(cam.id, cam.os_index, 'STOP')

                managed_cams = [c for c in db_cameras if c.status != 'OFF']
                running_indices = []
                
                if camera_system:
                    for cid, runner in list(camera_system.cameras.items()):
                        if getattr(runner, 'is_running', False):
                            try:
                                src = getattr(runner.stream, 'source', None)
                                if src is not None:
                                    idx = int(src)
                                    if platform.system() == "Linux" and not os.path.exists(f"/dev/video{idx}"):
                                        self._sync_system(cid, idx, 'STOP')
                                    else:
                                        running_indices.append(idx)
                            except: pass

                alive_unmanaged_indices = []
                for idx in range(self.max_scan_index + 1):
                    if idx in running_indices: continue
                    if check_physical_device(idx):
                        alive_unmanaged_indices.append(idx)

                running_db_cams = []
                for cam in managed_cams:
                    runner = camera_system.cameras.get(cam.id) if camera_system else None
                    if runner and getattr(runner, 'is_running', False):
                        running_db_cams.append(cam)
                        is_conn = 1 if getattr(runner, 'is_connected', False) else 0
                        if cam.status != 'ACTIVE' or cam.is_connected != is_conn:
                            self._update_db(db, cam, 'ACTIVE', is_conn)
                
                orphan_cams = [c for c in managed_cams if c not in running_db_cams]

                for idx in alive_unmanaged_indices:
                    reused_cam = None
                    for i, c in enumerate(orphan_cams):
                        if c.os_index == idx:
                            reused_cam = orphan_cams.pop(i)
                            break
                    
                    if not reused_cam and orphan_cams:
                        # [CHỐNG NHẢY GIAO DIỆN]: Ép luôn luôn lấy Camera cũ nhất (ID nhỏ nhất)
                        orphan_cams.sort(key=lambda x: x.id)
                        reused_cam = orphan_cams.pop(0)

                    if reused_cam:
                        print(f"♻️ [Re-Assign] Phục hồi luồng (DB ID: {reused_cam.id}) cho cổng /dev/video{idx}...")
                        reused_cam.os_index = idx
                        reused_cam.device_path = str(idx)
                        db.commit()
                        self._update_db(db, reused_cam, 'ACTIVE', 0)
                        self._sync_system(reused_cam.id, idx, 'START')
                        self.pending_new_cam_cycles.pop(idx, None)
                    else:
                        cycles = self.pending_new_cam_cycles.get(idx, 0) + 1
                        self.pending_new_cam_cycles[idx] = cycles
                        
                        if cycles >= 2:
                            print(f"🎉 [New Device] Phát hiện Camera mới tinh ở cổng {idx}. Thêm vào DB...")
                            new_cam = self._create_camera(db, idx)
                            if new_cam:
                                self._sync_system(new_cam.id, idx, 'START')
                            self.pending_new_cam_cycles.pop(idx, None)
                        else:
                            print(f"⏳ [Debounce] Cổng /dev/video{idx} có tín hiệu. Đang chờ ổn định nguồn điện...")

                for orphan in orphan_cams:
                    if orphan.status == 'ACTIVE':
                        print(f"❌ [Disconnect] Camera (DB ID: {orphan.id}) bị rút cáp hoặc sụt nguồn.")
                        self._update_db(db, orphan, 'DISCONNECTED', 0)

            except Exception as e: 
                traceback.print_exc()
            finally:
                if db: db.close()
            
            for _ in range(self.interval):
                if not self.is_running: break
                time.sleep(1)

    def _update_db(self, db, cam, status, is_connected):
        try:
            update_data = schemas.CameraUpdate(status=status, is_connected=is_connected)
            camera_crud.update(db, db_obj=cam, obj_in=update_data)
        except: pass

    def _create_camera(self, db, idx):
        try:
            cam_in = {
                "name": f"Camera Local {idx}", "display_name": f"Camera Local {idx}",
                "unique_id": f"CAM_AUTO_{idx}_{int(time.time())}", "device_id": str(idx),
                "device_path": str(idx), "os_index": idx,
                "status": "ACTIVE", "is_connected": 1, "rtsp_url": ""
            }
            return camera_crud.upsert(db, cam_in)
        except: return None

    def _sync_system(self, cam_id, idx, action):
        try:
            if action == 'START':
                old_cam = camera_system.cameras.get(cam_id)
                if old_cam and getattr(old_cam, 'is_running', False): return 
                if old_cam:
                    camera_system.stop_camera(cam_id)
                    time.sleep(0.5)
                if cam_id not in camera_system.cameras:
                    camera_system.add_camera(cam_id, idx)
            elif action == 'STOP':
                camera_system.stop_camera(cam_id)
        except: pass

upsert_camera_worker = UpsertCameraWorker(interval=5, max_scan_index=4)