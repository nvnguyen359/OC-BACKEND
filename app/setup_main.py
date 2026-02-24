# app/setup_main.py

import sys
import os
import asyncio
from pathlib import Path
import cv2
import uvicorn
# -----------------------------------------------------------------------------
# 2. IMPORTS (Sau khi đã setup path)
# -----------------------------------------------------------------------------
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# 1. SETUP PATH (PHẢI LÀM ĐẦU TIÊN)
# -----------------------------------------------------------------------------
# Lấy đường dẫn file hiện tại để tìm ra Project Root
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent # Lên 2 cấp: app -> root
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


# Import Service nội bộ
try:
    from app.services.network_service import network_service
except ImportError as e:
    print(f"❌ Setup Error: Cannot import network_service. Details: {e}")
    sys.exit(1)

# -----------------------------------------------------------------------------
# 3. CẤU HÌNH APP
# -----------------------------------------------------------------------------
# Thư mục chứa giao diện HTML setup
HOTSPOT_DIR = current_file.parent / "hotspot"

app = FastAPI(title="Wifi Setup Mode")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount thư mục static để load css/js
app.mount("/static", StaticFiles(directory=str(HOTSPOT_DIR)), name="static")

# -----------------------------------------------------------------------------
# 4. MODELS
# -----------------------------------------------------------------------------
class WifiRequest(BaseModel):
    ssid: str
    password: str

class CameraTestRequest(BaseModel):
    rtsp: str

# -----------------------------------------------------------------------------
# 5. ROUTES
# -----------------------------------------------------------------------------

@app.get("/")
async def setup_dashboard():
    """Trả về giao diện Setup (index.html)"""
    index_path = HOTSPOT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"error": "Setup UI not found at " + str(index_path)}, status_code=404)


@app.get("/setup/scan")
async def scan_wifi():
    """Quét Wifi xung quanh"""
    try:
        networks = network_service.scan_wifi()
        # Sắp xếp theo độ mạnh sóng (Signal strength)
        networks.sort(key=lambda x: x.get('signal', 0), reverse=True)
        return {"networks": networks}
    except Exception as e:
        print(f"Scan Error: {e}")
        return {"networks": [], "error": str(e)}


@app.post("/setup/connect")
async def connect_wifi(payload: WifiRequest, background_tasks: BackgroundTasks):
    """
    Xử lý kết nối Wifi:
    1. Thử kết nối.
    2. Nếu OK -> Hẹn giờ Reboot.
    3. Nếu Fail -> Bật lại Hotspot ngay lập tức.
    """
    print(f"🔄 Setup: Attempting to connect to '{payload.ssid}'...")

    # Gọi hàm kết nối (Blocking call để lấy kết quả thực tế)
    success = network_service.connect_wifi(payload.ssid, payload.password)

    if success:
        print("✅ Setup: Connected! Scheduling reboot...")
        background_tasks.add_task(reboot_sequence)
        return {
            "status": "success",
            "message": "Kết nối thành công! Thiết bị sẽ khởi động lại sau 5 giây."
        }
    else:
        print("❌ Setup: Connect Failed (Wrong Pass or Timeout). Re-enabling Hotspot...")
        
        # [QUAN TRỌNG] Bật lại Hotspot ngay lập tức để người dùng không bị mất kết nối
        network_service.enable_hotspot()

        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Không thể kết nối tới '{payload.ssid}'. Vui lòng kiểm tra mật khẩu."
            }
        )


async def reboot_sequence():
    """Đợi 5s rồi reboot"""
    await asyncio.sleep(5)
    print("🔄 System Rebooting...")
    network_service.reboot_system()


@app.post("/setup/test-camera")
async def test_camera(payload: CameraTestRequest):
    """Kiểm tra luồng RTSP"""
    print(f"📷 Testing Camera: {payload.rtsp}")
    try:
        # Mở luồng camera để test
        cap = cv2.VideoCapture(payload.rtsp)
        
        if not cap.isOpened():
            return {"ok": False, "error": "Connection Refused (Check IP/Port)"}

        ret, frame = cap.read()
        cap.release()

        if ret:
            h, w = frame.shape[:2]
            return {"ok": True, "width": w, "height": h}
        else:
            return {"ok": False, "error": "Stream opened but no data received."}

    except Exception as e:
        return {"ok": False, "error": str(e)}


# -----------------------------------------------------------------------------
# 6. ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("⚠️  RUNNING IN SETUP MODE")
    print("📡  Hotspot SSID: ORDER_CAMERA_SETUP")
    print("🌐  Config URL:   http://10.42.0.1:8000") # IP Gateway mặc định của Hotspot
    
    # [FIX] Chạy app trực tiếp (app object), host 0.0.0.0 để access từ ngoài
    # Không dùng "app.main:app" vì đó là App chính, đây là App Setup
    uvicorn.run(app, host="0.0.0.0", port=8000)