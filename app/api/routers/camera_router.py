# app/routers/camera_router.py
import asyncio
import json
import time
import cv2
import numpy as np
from datetime import datetime
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import StreamingResponse, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db import schemas
from app.db.session import get_db, SessionLocal
from app.services.camera_service import CameraService
from app.utils.response import response_success

# Auth deps
from app.core.security import decode_access_token
from app.crud.user_crud import user_crud

# Import hệ thống worker (Đã chạy ngầm)
from app.workers.camera_worker import camera_system 

router = APIRouter(prefix="/cameras", tags=["cameras"])

# Cấu hình Token OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# --- HELPER: TẠO ẢNH LOADING ---
def create_placeholder_image():
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "OFFLINE / LOADING...", (180, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()

PLACEHOLDER_BYTES = create_placeholder_image()

# --- MODEL RESPONSE ---
class CameraListResponse(BaseModel):
    code: int = 200
    mes: str = "success"
    data: List[schemas.CameraOut]

# =========================================================
# 0. AUTH DEPENDENCIES
# =========================================================

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Lấy thông tin User hiện tại từ Token.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    username = payload.get("sub")
    user = user_crud.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# =========================================================
# 1. WEBSOCKET
# =========================================================

async def get_ws_user(token: str):
    if not token: return None
    try:
        payload = decode_access_token(token)
        if not payload: return None
        username = payload.get("sub")
        db = SessionLocal()
        try:
            user = user_crud.get_by_username(db, username)
            if user and user.is_active == 1:
                return user
        finally:
            db.close()
    except Exception as e:
        print(f"❌ [WS Auth] Error: {e}")
        return None
    return None

@router.websocket("/ws")
async def websocket_ai_overlay(
    websocket: WebSocket,
    token: str = Query(..., description="JWT Token"),
    camera_id: Optional[int] = Query(None)
):
    user = await get_ws_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    target_cam_id = camera_id
    
    tick_count = 0 
    last_event_timestamps = {}

    try:
        while True:
            tick_count += 1
            if tick_count % 10 == 0:
                stats_msg = {"type": "system_stats", "data": camera_system.system_stats}
                try: await websocket.send_json(stats_msg)
                except: pass

                active_orders = []
                for cid, cam in camera_system.cameras.items():
                    if cam.is_running and cam.recording:
                        active_orders.append({
                            "camera_id": cid,
                            "order_id": cam.current_order_db_id,
                            "code": cam.machine.current_code,
                            "start_time": datetime.fromtimestamp(cam.rec_start_time).isoformat(),
                            "path_avatar": cam.current_avatar_path 
                        })
                try: await websocket.send_json({ "type": "active_orders", "data": active_orders })
                except: pass

            active_cameras = list(camera_system.cameras.items())
            for cam_id, cam in active_cameras:
                if target_cam_id is not None and cam_id != target_cam_id: continue
                if not cam.is_running: continue

                if cam.ai_metadata:
                    msg = {"camera_id": cam_id, "metadata": cam.ai_metadata, "timestamp": str(time.time())}
                    qr_objects = [obj for obj in cam.ai_metadata if obj.get("type") in ["qrcode", "code"]]
                    if qr_objects:
                        msg["event"] = "QR_SCANNED"
                        msg["data"] = { "code": qr_objects[0].get("code"), "type": qr_objects[0].get("code_type")}
                    try: await websocket.send_json(msg)
                    except: break

                if hasattr(cam, 'stream_metadata') and cam.stream_metadata:
                    evt_data = cam.stream_metadata
                    current_evt_ts = evt_data.get("ts", 0)
                    last_sent_ts = last_event_timestamps.get(cam_id, 0)
                    if current_evt_ts > last_sent_ts:
                        msg_evt = {"camera_id": cam_id, "event": evt_data.get("event"), "data": evt_data.get("data"), "timestamp": str(time.time())}
                        try: await websocket.send_json(msg_evt)
                        except: break
                        last_event_timestamps[cam_id] = current_evt_ts

            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.05)
                new_id = data.get("camera_id") or data.get("cam_id")
                if new_id: target_cam_id = int(new_id)
            except asyncio.TimeoutError: pass 
            except WebSocketDisconnect: return 
            except Exception: pass 

    except Exception as e:
        pass
    finally:
        try: await websocket.close() 
        except: pass

# =========================================================
# 2. STREAM & SNAPSHOT
# =========================================================

@router.get("/{cam_id}/stream")
async def get_camera_stream(cam_id: int):
    cam = camera_system.cameras.get(cam_id)
    if not cam: raise HTTPException(status_code=404, detail="Camera not active in background")
    
    async def iterfile():
        while True:
            try:
                frame_bytes = cam.get_jpeg()
                if frame_bytes:
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                else:
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + PLACEHOLDER_BYTES + b'\r\n')
                await asyncio.sleep(0.03 if frame_bytes else 0.2)
            except GeneratorExit: break
            except Exception: break
    return StreamingResponse(iterfile(), media_type="multipart/x-mixed-replace;boundary=frame")

@router.get("/{cam_id}/snapshot")
def get_camera_snapshot(cam_id: int):
    cam = camera_system.cameras.get(cam_id)
    if cam and cam.is_running:
        img_bytes = cam.get_snapshot() if hasattr(cam, 'get_snapshot') else cam.get_jpeg()
        if img_bytes: return Response(content=img_bytes, media_type="image/jpeg")
    return Response(content=PLACEHOLDER_BYTES, media_type="image/jpeg")

@router.get("/{cam_id}/ai-overlay")
def get_ai_overlay_http(cam_id: int):
    cam = camera_system.cameras.get(cam_id)
    return cam.ai_metadata if cam else []

# =========================================================
# 3. CONTROL (CONNECT / DISCONNECT)
# =========================================================

@router.post("/{cam_id}/connect")
def connect_camera(
    cam_id: int, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    [START] Bật Camera: Cập nhật DB ACTIVE & Chạy Worker
    """
    svc = CameraService(db)
    
    # 1. Update DB -> ACTIVE (Cho cả User và Admin)
    cam = svc.connect_camera(cam_id)
    if not cam: raise HTTPException(404, "Camera not found")

    source = cam.device_path or cam.rtsp_url or cam.device_id
    if str(source).isdigit(): source = int(source)
    
    try: 
        # 2. Start Worker
        camera_system.add_camera(cam_id, source)
    except Exception as e:
        svc.disconnect_camera(cam_id) # Rollback nếu lỗi
        raise HTTPException(500, f"Worker Error: {e}")
        
    return response_success(data=cam)


@router.post("/{cam_id}/disconnect")
def disconnect_camera(
    cam_id: int, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    [STOP] Tắt Camera:
    - Nếu là ADMIN: Set trạng thái 'OFF' -> Worker sẽ KHÔNG tự động quét/bật lại.
    - Nếu là USER thường: Set 'DISCONNECTED'.
    """
    svc = CameraService(db)
    
    is_admin = getattr(user, "is_superuser", False) or getattr(user, "role", "").upper() == "ADMIN"
    
    new_status = "OFF" if is_admin else "DISCONNECTED"
    
    cam = svc.disconnect_camera(cam_id)
    
    if is_admin and cam:
        cam.status = new_status
        db.commit()
        db.refresh(cam)
    
    camera_system.stop_camera(cam_id)
    time.sleep(0.5)
    
    role = "ADMIN" if is_admin else "USER"
    print(f"🛑 [{role} {user.username}] Đã tắt cam: {cam_id} (Status: {new_status})")
    
    # [FIX] Đánh lừa Pydantic Response
    # Nếu là OFF thì trả về DISCONNECTED để không bị lỗi 500 Validation Error
    if cam.status == 'OFF':
        cam.status = 'DISCONNECTED'
        
    return response_success(data=cam)


@router.post("/{cam_id}/record")
def control_recording(cam_id: int, action: str = "start", code: str = None, db: Session = Depends(get_db)):
    cam_runtime = camera_system.cameras.get(cam_id)
    if not cam_runtime: raise HTTPException(404, "Camera is not running")
    
    if action == "start":
        cam_runtime.start_recording(code=code or "MANUAL")
    else:
        cam_runtime.stop_recording()
    
    return response_success(data={"status": "success", "recording": cam_runtime.recording})


# =========================================================
# 4. BASIC CRUD
# =========================================================

@router.get("/{cam_id}")
def get_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    cam = svc.get_camera(cam_id)
    if not cam: raise HTTPException(404, "Camera not found")
    
    # [FIX] Tránh lỗi 500 nếu Status='OFF' mà Schema không cho phép
    if cam.status == 'OFF':
        cam.status = 'DISCONNECTED'

    # Validate bằng Pydantic sau khi đã patch status
    cam_data = schemas.CameraOut.model_validate(cam).model_dump()
    
    real_cam = camera_system.cameras.get(cam_id)
    
    if real_cam:
        cam_data['is_connected'] = True
        cam_data['recording_state'] = 'MANUAL' if real_cam.recording else 'IDLE'
        current_code = real_cam.machine.current_code if hasattr(real_cam, 'machine') else None
        if current_code and current_code != "MANUAL":
            cam_data['recording_state'] = 'AUTO'
            cam_data['active_order_code'] = current_code
    else:
        cam_data['is_connected'] = False
        cam_data['recording_state'] = 'DISCONNECTED'
    
    return response_success(data=cam_data)

@router.post("")
def create_camera(cam: schemas.CameraCreate, db: Session = Depends(get_db)):
    return response_success(CameraService(db).create_camera(cam))

@router.get("", response_model=CameraListResponse)
def get_all_cameras(db: Session = Depends(get_db), skip: int = 0, limit: int = 100,all:bool = True):
    cams = CameraService(db).get_all_cameras(skip, limit, all)
    
    # [FIX CRITICAL] Xử lý lỗi 500 Validation Error
    # Schema CameraOut hiện tại có thể chỉ chấp nhận 'ACTIVE' | 'DISCONNECTED' | 'ERROR'
    # Nếu status là 'OFF', Pydantic sẽ throw error.
    # Ta cần map 'OFF' -> 'DISCONNECTED' cho tầng hiển thị.
    for cam in cams:
        if cam.status == 'OFF':
            cam.status = 'DISCONNECTED'
            
    return response_success(cams)

@router.patch("/{cam_id}")
def update_camera(cam_id: int, cam_in: schemas.CameraUpdate, db: Session = Depends(get_db)):
    updated_cam = CameraService(db).update_camera(cam_id, cam_in)
    
    # [FIX] Patch cả ở đây để tránh lỗi khi update xong trả về
    if updated_cam.status == 'OFF':
        updated_cam.status = 'DISCONNECTED'
        
    return response_success(updated_cam)

@router.delete("/{cam_id}")
def delete_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    camera_system.stop_camera(cam_id)
    return response_success(svc.delete_camera(cam_id))

@router.delete("")
def delete_all_cameras(db: Session = Depends(get_db)):
    svc = CameraService(db)
    camera_system.shutdown()
    camera_system.__init__() 
    return response_success(data={"deleted": svc.delete_all_cameras()})