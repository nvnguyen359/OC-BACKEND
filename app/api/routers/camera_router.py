# app/api/routers/camera_router.py
import asyncio
import json
import time
import cv2
import numpy as np
from datetime import datetime
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import StreamingResponse, Response
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

# --- HELPER: TẠO ẢNH LOADING ---
def create_placeholder_image():
    # Tạo ảnh xám đen kích thước 640x480
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Viết chữ thông báo
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
# 1. WEBSOCKET: AI EVENTS + SYSTEM STATS + ACTIVE ORDERS
# =========================================================

async def get_ws_user(token: str):
    """Xác thực Token JWT cho WebSocket"""
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
    camera_id: Optional[int] = Query(None) # Client có thể gửi ?camera_id=...
):
    """
    WebSocket Đa Năng:
    1. Gửi AI Metadata (Human Box, QR Code).
    2. Gửi System Stats (CPU, RAM).
    3. [REALTIME] Push Active Orders List (Danh sách đang đóng gói).
    4. [EVENT] Gửi sự kiện nghiệp vụ (Created/Stopped) dựa trên Timestamp.
    """
    # 1. Auth
    user = await get_ws_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    
    # Xác định camera mục tiêu
    target_cam_id = camera_id
    print(f"✅ [WS] Connected: {user.username}")

    tick_count = 0 
    
    # [FIX] Theo dõi timestamp của event cuối cùng đã gửi để tránh lặp/mất tin
    # Dict lưu {cam_id: last_event_timestamp (float)}
    last_event_timestamps = {}

    try:
        while True:
            tick_count += 1

            # -----------------------------------------------------------
            # [MỚI] PUSH DANH SÁCH PACKING ORDERS & STATS (Mỗi 0.5s)
            # -----------------------------------------------------------
            if tick_count % 10 == 0:
                # 1. System Stats
                stats_msg = {
                    "type": "system_stats",
                    "data": camera_system.system_stats
                }
                try: await websocket.send_json(stats_msg)
                except: pass

                # 2. Active Orders List (Lấy trực tiếp từ RAM Worker)
                # Giúp Client hiển thị danh sách ngay lập tức, không cần gọi API
                active_orders = []
                for cid, cam in camera_system.cameras.items():
                    # Chỉ lấy camera đang chạy và đang trong trạng thái PACKING
                    if cam.is_running and cam.recording:
                        active_orders.append({
                            "camera_id": cid,
                            "order_id": cam.current_order_db_id,
                            "code": cam.machine.current_code,
                            # Chuyển start_time sang ISO string
                            "start_time": datetime.fromtimestamp(cam.rec_start_time).isoformat(),
                            # Lấy avatar tạm từ RAM (cập nhật tức thì)
                            "path_avatar": cam.current_avatar_path 
                        })
                
                # Gửi danh sách xuống Client
                try: await websocket.send_json({ "type": "active_orders", "data": active_orders })
                except: pass

            # -----------------------------------------------------------
            # B. Gửi Metadata & Events từ các Camera (Realtime)
            # -----------------------------------------------------------
            active_cameras = list(camera_system.cameras.items())
            
            for cam_id, cam in active_cameras:
                # Nếu client đang focus 1 cam cụ thể, bỏ qua cam khác
                if target_cam_id is not None and cam_id != target_cam_id:
                    continue

                if not cam.is_running: continue

                # 1. Gửi AI Metadata (Bounding Box) - Realtime liên tục
                if cam.ai_metadata:
                    msg = {
                        "camera_id": cam_id,
                        "metadata": cam.ai_metadata, 
                        "timestamp": str(time.time())
                    }

                    # Logic QR_SCANNED từ Metadata (Backup cho realtime view)
                    qr_objects = [obj for obj in cam.ai_metadata if obj.get("type") in ["qrcode", "code"]]
                    if qr_objects:
                        msg["event"] = "QR_SCANNED"
                        msg["data"] = { 
                            "code": qr_objects[0].get("code"),
                            "type": qr_objects[0].get("code_type")
                        }
                    
                    try: await websocket.send_json(msg)
                    except: break

                # 2. [FIX QUAN TRỌNG] Gửi Sự kiện Nghiệp vụ (ORDER_CREATED/STOPPED)
                # Check xem camera có event mới không bằng timestamp
                if hasattr(cam, 'stream_metadata') and cam.stream_metadata:
                    evt_data = cam.stream_metadata
                    # Lấy timestamp của sự kiện từ Worker (mặc định là 0 nếu không có)
                    current_evt_ts = evt_data.get("ts", 0)
                    
                    # Lấy timestamp đã gửi lần trước cho cam này
                    last_sent_ts = last_event_timestamps.get(cam_id, 0)
                    
                    # Nếu timestamp mới lớn hơn cái cũ -> Có sự kiện mới -> Gửi
                    if current_evt_ts > last_sent_ts:
                        msg_evt = {
                            "camera_id": cam_id,
                            "event": evt_data.get("event"),
                            "data": evt_data.get("data"),
                            "timestamp": str(time.time())
                        }
                        try: await websocket.send_json(msg_evt)
                        except: break
                        
                        # Cập nhật timestamp đã gửi để không gửi lại
                        last_event_timestamps[cam_id] = current_evt_ts

            # --- C. Check tin nhắn từ Client (Non-blocking) ---
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.05)
                # Client chuyển cam: {"camera_id": 2}
                new_id = data.get("camera_id") or data.get("cam_id")
                if new_id: target_cam_id = int(new_id)
            except asyncio.TimeoutError: pass 
            except WebSocketDisconnect: return 
            except Exception: pass 

    except Exception as e:
        print(f"❌ [WS] Error: {e}")
    finally:
        try: await websocket.close() 
        except: pass


# =========================================================
# 2. STREAM VIDEO & SNAPSHOT
# =========================================================

@router.get("/{cam_id}/stream")
async def get_camera_stream(cam_id: int):
    """MJPEG Stream Endpoint"""
    cam = camera_system.get_camera(cam_id)
    if not cam: 
        # Nếu cam chưa chạy trong system, có thể do vừa khởi động hoặc lỗi
        # Tuy nhiên với logic background mode, ta vẫn check trong DB xem có nên chạy không
        # Ở đây đơn giản trả về lỗi để FE retry
        raise HTTPException(status_code=404, detail="Camera not active in background")
    
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
    cam = camera_system.get_camera(cam_id)
    if cam and cam.is_running:
        img_bytes = cam.get_snapshot() if hasattr(cam, 'get_snapshot') else cam.get_jpeg()
        if img_bytes: return Response(content=img_bytes, media_type="image/jpeg")
    return Response(content=PLACEHOLDER_BYTES, media_type="image/jpeg")


# =========================================================
# 3. HTTP POLLING FALLBACK & CONTROL (FIXED LOGIC)
# =========================================================

@router.get("/{cam_id}/ai-overlay")
def get_ai_overlay_http(cam_id: int):
    cam = camera_system.get_camera(cam_id)
    return cam.ai_metadata if cam else []

@router.post("/{cam_id}/connect")
def connect_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    
    # 1. Chỉ lấy thông tin camera, chưa vội update
    cam = svc.get_camera(cam_id)
    if not cam: raise HTTPException(404, "Camera not found")

    source = cam.device_path or cam.rtsp_url or cam.device_id
    if str(source).isdigit(): source = int(source)
    
    try: 
        # 2. [FIX] Đảm bảo DB là ACTIVE để worker không bị kill
        # Sử dụng update_camera để set status
        svc.update_camera(cam_id, schemas.CameraUpdate(status='ACTIVE'))
        
        # 3. Add vào system (Hàm add_camera trong system đã fix để không restart nếu đang chạy)
        camera_system.add_camera(cam_id, source)
        
    except Exception as e:
        raise HTTPException(500, f"Worker Error: {e}")
        
    return response_success(data=cam)


@router.post("/{cam_id}/disconnect")
def disconnect_camera(cam_id: int, db: Session = Depends(get_db)):
    """
    [FIX] Logic Disconnect:
    - Chỉ trả về success để Frontend dừng stream.
    - KHÔNG gọi svc.disconnect_camera() (vì hàm đó set DB = DISCONNECTED -> kill worker).
    - Giữ worker chạy ngầm.
    """
    # svc = CameraService(db)
    # cam = svc.disconnect_camera(cam_id)  <-- BỎ DÒNG NÀY
    
    return response_success(data={"status": "view_disconnected", "message": "Camera running in background"})


@router.post("/{cam_id}/record")
def control_recording(cam_id: int, action: str = "start", code: str = None, db: Session = Depends(get_db)):
    cam_runtime = camera_system.get_camera(cam_id)
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
    
    # --- [FIX] Lấy trạng thái thực từ Worker ---
    cam_data = schemas.CameraOut.model_validate(cam).model_dump()
    real_cam = camera_system.get_camera(cam_id)
    
    if real_cam:
        cam_data['is_connected'] = True
        cam_data['recording_state'] = 'MANUAL' if real_cam.recording else 'IDLE'
        
        # [FIX CRASH] Sử dụng real_cam.machine.current_code thay vì real_cam.order_code
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
def get_all_cameras(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return response_success(CameraService(db).get_all_cameras(skip, limit))

@router.patch("/{cam_id}")
def update_camera(cam_id: int, cam_in: schemas.CameraUpdate, db: Session = Depends(get_db)):
    return response_success(CameraService(db).update_camera(cam_id, cam_in))

@router.delete("/{cam_id}")
def delete_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    
    # [FIX] Khi xóa hẳn camera mới dừng Worker
    camera_system.stop_camera(cam_id)
    
    return response_success(svc.delete_camera(cam_id))

@router.delete("")
def delete_all_cameras(db: Session = Depends(get_db)):
    svc = CameraService(db)
    camera_system.shutdown()
    camera_system.__init__() 
    return response_success(data={"deleted": svc.delete_all_cameras()})