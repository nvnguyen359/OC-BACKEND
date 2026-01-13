# app/api/routers/camera_router.py
import asyncio
import json
import time
import cv2
import numpy as np
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
# 1. WEBSOCKET: AI EVENTS + SYSTEM STATS
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
    3. Nhận lệnh chuyển Camera từ Client.
    """
    # 1. Auth
    user = await get_ws_user(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    
    # Xác định camera mục tiêu (Nếu client chỉ định)
    target_cam_id = camera_id
    if target_cam_id:
        print(f"✅ [WS] Client connected: {user.username} -> Watching Cam {target_cam_id}")
    else:
        print(f"✅ [WS] Client connected: {user.username} -> Dashboard Mode")

    # Biến đếm để điều tiết tốc độ gửi System Stats
    tick_count = 0 

    try:
        while True:
            # --- A. Gửi System Stats (Mỗi 10 tick ~ 0.5s) ---
            # [BỔ SUNG] Gửi thông số RAM/CPU xuống Client
            tick_count += 1
            if tick_count % 10 == 0:
                stats_msg = {
                    "type": "system_stats",
                    "data": camera_system.system_stats # Lấy từ biến toàn cục bên Worker
                }
                try: 
                    await websocket.send_json(stats_msg)
                except RuntimeError: 
                    return # Socket đóng thì thoát ngay
                except Exception: 
                    pass

            # --- B. Gửi AI Metadata (Camera) ---
            active_cameras = list(camera_system.cameras.items())
            
            for cam_id, cam in active_cameras:
                # Nếu Client đang focus vào 1 camera cụ thể, bỏ qua các camera khác
                if target_cam_id is not None and cam_id != target_cam_id:
                    continue

                if cam.is_running and cam.ai_metadata:
                    # Cấu trúc tin nhắn khớp với Client
                    msg = {
                        "camera_id": cam_id,
                        "metadata": cam.ai_metadata, # List các box (Human, QR Box)
                        "timestamp": str(time.time())
                    }

                    # --- LOGIC EVENT QR CODE ---
                    # Tìm trong metadata xem có QR/Barcode không?
                    qr_objects = [obj for obj in cam.ai_metadata if obj.get("type") in ["qrcode", "code"]]
                    
                    if qr_objects:
                        # Nếu có, bắn thêm Event 'QR_SCANNED' kèm dữ liệu mã
                        first_code = qr_objects[0]
                        msg["event"] = "QR_SCANNED"
                        msg["data"] = { 
                            "code": first_code.get("code_content"),
                            "type": first_code.get("code_type")
                        }

                    # [FIX QUAN TRỌNG] Bọc send_json trong try/except để bắt lỗi Socket Closed
                    try:
                        await websocket.send_json(msg)
                    except RuntimeError:
                        # Lỗi này xảy ra khi Client ngắt kết nối đột ngột
                        return 
                    except Exception:
                        return

            # --- C. Check tin nhắn từ Client (Non-blocking) ---
            # Ví dụ: Client chuyển sang xem Camera khác
            try:
                # Chờ tin nhắn trong 0.05s (Tạo độ trễ ~20FPS cho loop)
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.05)
                
                # Client gửi: {"camera_id": 2}
                new_id = data.get("camera_id") or data.get("cam_id")
                if new_id:
                    target_cam_id = int(new_id)
            
            except asyncio.TimeoutError:
                pass # Không có tin nhắn -> tiếp tục loop
            except WebSocketDisconnect:
                print(f"🔌 [WS] Client disconnected: {user.username}")
                return # Thoát vòng lặp
            except Exception:
                pass 

    except WebSocketDisconnect:
        print(f"🔌 [WS] Disconnected: {user.username}")
    except Exception as e:
        print(f"❌ [WS] Unexpected Error: {e}")
    finally:
        # Cố gắng đóng socket nếu chưa đóng
        try: await websocket.close() 
        except: pass


# =========================================================
# 2. STREAM VIDEO & SNAPSHOT
# =========================================================

@router.get("/{cam_id}/stream")
def get_camera_stream(cam_id: int):
    """
    MJPEG Stream Endpoint.
    Trả về luồng video (đã được resize 720p ở worker để giảm lag).
    """
    cam = camera_system.get_camera(cam_id)
    
    # Nếu worker chưa chạy, trả về lỗi 404
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not active")
    
    def iterfile():
        while True:
            try:
                # Lấy ảnh JPEG từ worker (đã resize)
                frame_bytes = cam.get_jpeg()
                
                if frame_bytes:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                else:
                    # Nếu chưa có ảnh (đang khởi động), gửi ảnh Placeholder
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + PLACEHOLDER_BYTES + b'\r\n')
                    time.sleep(0.1) # Gửi chậm khi loading
                
                # Sleep cực ngắn để kiểm soát tốc độ stream
                time.sleep(0.01)
            except Exception:
                # Client ngắt kết nối stream -> Thoát vòng lặp
                break

    return StreamingResponse(iterfile(), media_type="multipart/x-mixed-replace;boundary=frame")


@router.get("/{cam_id}/snapshot")
def get_camera_snapshot(cam_id: int):
    """
    [MỚI] Lấy 1 ảnh tĩnh (Snapshot) mới nhất từ Worker.
    Dùng để hiển thị background khi Client không muốn load cả Video Stream.
    """
    cam = camera_system.get_camera(cam_id)
    
    # 1. Nếu Camera đang chạy -> Lấy ảnh từ RAM
    if cam and cam.is_running:
        # Ưu tiên dùng get_snapshot (nét hơn), nếu chưa có thì dùng get_jpeg
        if hasattr(cam, 'get_snapshot'):
            img_bytes = cam.get_snapshot()
        else:
            img_bytes = cam.get_jpeg() # Fallback

        if img_bytes:
            return Response(content=img_bytes, media_type="image/jpeg")
    
    # 2. Nếu Camera không chạy hoặc chưa có ảnh -> Trả về ảnh mặc định
    return Response(content=PLACEHOLDER_BYTES, media_type="image/jpeg")


# =========================================================
# 3. HTTP POLLING FALLBACK (Cho UI vẽ Box nếu không dùng WS)
# =========================================================

@router.get("/{cam_id}/ai-overlay")
def get_ai_overlay_http(cam_id: int):
    cam = camera_system.get_camera(cam_id)
    if not cam: return []
    return cam.ai_metadata


# =========================================================
# 4. CONTROL API (CONNECT / DISCONNECT / RECORD)
# =========================================================

@router.post("/{cam_id}/connect")
def connect_camera(cam_id: int, db: Session = Depends(get_db)):
    """Bật Camera (Khởi động Worker)"""
    svc = CameraService(db)
    
    # 1. Update DB Status -> ACTIVE
    cam = svc.connect_camera(cam_id)
    if not cam: raise HTTPException(404, "Camera not found")

    # 2. Lấy Source (Ưu tiên Device Path -> RTSP -> ID)
    source = cam.device_path or cam.rtsp_url or cam.device_id
    
    # Nếu là số (Index 0, 1...) -> Convert sang int
    if str(source).isdigit(): source = int(source)
    
    # 3. Kích hoạt Worker (Nếu chưa chạy)
    try:
        camera_system.add_camera(cam_id, source)
    except Exception as e:
        svc.disconnect_camera(cam_id)
        raise HTTPException(500, f"Worker Error: {e}")
    
    return response_success(data=cam)


@router.post("/{cam_id}/disconnect")
def disconnect_camera(cam_id: int, db: Session = Depends(get_db)):
    """
    Client gọi API này khi người dùng tắt xem camera.
    QUAN TRỌNG: 
    - CHỈ cập nhật trạng thái UI trong DB (is_connected = 0).
    - KHÔNG TẮT Worker (Worker vẫn chạy ngầm để bắt QR).
    """
    svc = CameraService(db)
    
    # [LOGIC CŨ ĐÃ BỎ]: real_cam.stop() -> Gây mất kết nối hoàn toàn
    
    # Chỉ update status DB
    cam = svc.disconnect_camera(cam_id)
    
    return response_success(data=cam)


@router.post("/{cam_id}/record")
def control_recording(cam_id: int, action: str = "start", code: str = None, db: Session = Depends(get_db)):
    """Điều khiển ghi hình Video"""
    cam_runtime = camera_system.get_camera(cam_id)
    
    if not cam_runtime:
         raise HTTPException(status_code=404, detail="Camera is not running (Worker offline)")
    
    if action == "start":
        cam_runtime.start_recording(order_code=code or "MANUAL")
    else:
        cam_runtime.stop_recording()
    
    return response_success(data={"status": "success", "recording": cam_runtime.recording})


# =========================================================
# 5. BASIC CRUD (GET, LIST, CREATE, UPDATE, DELETE)
# =========================================================

@router.get("/{cam_id}")
def get_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    cam = svc.get_camera(cam_id)
    if not cam: raise HTTPException(404, "Camera not found")
    
    # Merge trạng thái thực tế từ Worker
    cam_data = schemas.CameraOut.model_validate(cam).model_dump()
    real_cam = camera_system.get_camera(cam_id)
    
    if real_cam:
        # Nếu worker đang chạy
        cam_data['recording_state'] = 'MANUAL' if real_cam.recording else 'IDLE'
        if real_cam.order_code and real_cam.order_code != "MANUAL":
            cam_data['recording_state'] = 'AUTO'
            cam_data['active_order_code'] = real_cam.order_code
    else:
        # Worker không chạy
        cam_data['recording_state'] = 'DISCONNECTED'
    
    return response_success(data=cam_data)


@router.post("")
def create_camera(cam: schemas.CameraCreate, db: Session = Depends(get_db)):
    svc = CameraService(db)
    return response_success(svc.create_camera(cam))


@router.get("", response_model=CameraListResponse)
def get_all_cameras(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    svc = CameraService(db)
    return response_success(svc.get_all_cameras(skip, limit))


@router.patch("/{cam_id}")
def update_camera(cam_id: int, cam_in: schemas.CameraUpdate, db: Session = Depends(get_db)):
    svc = CameraService(db)
    return response_success(svc.update_camera(cam_id, cam_in))


@router.delete("/{cam_id}")
def delete_camera(cam_id: int, db: Session = Depends(get_db)):
    svc = CameraService(db)
    
    # Nếu xóa hẳn Camera khỏi hệ thống -> Thì mới Stop Worker
    real_cam = camera_system.get_camera(cam_id)
    if real_cam: 
        real_cam.stop()
        
    return response_success(svc.delete_camera(cam_id))


@router.delete("")
def delete_all_cameras(db: Session = Depends(get_db)):
    svc = CameraService(db)
    # Tắt toàn bộ hệ thống
    camera_system.shutdown()
    # Khởi tạo lại object rỗng
    camera_system.__init__() 
    
    return response_success(data={"deleted": svc.delete_all_cameras()})