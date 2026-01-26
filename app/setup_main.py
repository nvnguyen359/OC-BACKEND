# app/setup_main.py

import sys
import os
import asyncio
from pathlib import Path
import cv2 

# [FIX PATH] Tự động thêm root vào sys.path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent 
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles # [NEW] Import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import Service
from app.services.network_service import network_service

# Định nghĩa đường dẫn tới thư mục hotspot
HOTSPOT_DIR = current_file.parent / "hotspot"

app = FastAPI(title="Wifi Setup Mode", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# [NEW] Mount thư mục hotspot vào đường dẫn /static
# Để HTML có thể gọi: /static/style.css và /static/script.js
app.mount("/static", StaticFiles(directory=str(HOTSPOT_DIR)), name="static")

class WifiRequest(BaseModel):
    ssid: str
    password: str

class CameraTestRequest(BaseModel):
    rtsp: str

# --- ROUTER GIAO DIỆN CHÍNH ---
@app.get("/")
async def setup_dashboard():
    """Trả về file index.html nằm trong thư mục hotspot"""
    index_path = HOTSPOT_DIR / "index.html"
    return FileResponse(index_path)

# --- ROUTER WIFI ---
@app.get("/setup/scan")
async def scan_wifi():
    networks = network_service.scan_wifi()
    networks.sort(key=lambda x: x['signal'], reverse=True)
    return {"networks": networks}

@app.post("/setup/connect")
async def connect_wifi(payload: WifiRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(handle_reboot_sequence, payload.ssid, payload.password)
    return {"status": "connecting", "message": "Đang kết nối..."}

async def handle_reboot_sequence(ssid, password):
    print(f"🔄 Setup: Connecting to {ssid}...")
    success = network_service.connect_wifi(ssid, password)
    if success:
        print("✅ Setup: Wifi Connected! Rebooting system in 5s...")
        await asyncio.sleep(5)
        network_service.reboot_system()
    else:
        print("❌ Setup: Connect Failed.")

# --- ROUTER TEST CAMERA ---
@app.post("/setup/test-camera")
async def test_camera_connection(payload: CameraTestRequest):
    print(f"📷 Testing Camera: {payload.rtsp}")
    try:
        cap = cv2.VideoCapture(payload.rtsp)
        if not cap.isOpened():
            return {"ok": False, "error": "Không thể mở luồng (Connection Refused)"}
        
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            cap.release()
            return {"ok": True, "width": w, "height": h}
        else:
            cap.release()
            return {"ok": False, "error": "Mở được nhưng không đọc được Frame (No Data)"}
            
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    print("⚠️  RUNNING IN SETUP MODE (NO INTERNET) ⚠️")
    print("📡  Hotspot SSID: ORDER_CAMERA_SETUP")
    print("🌐  Config URL:   http://10.42.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)