# app/api/routers/setup_router.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.services.network_service import network_service
import asyncio

router = APIRouter(prefix="/setup", tags=["Setup"])

class WifiConnectRequest(BaseModel):
    ssid: str
    password: str

@router.get("/scan")
async def scan_wifi_networks():
    """API trả về danh sách Wifi để hiển thị lên Dropdown"""
    networks = network_service.scan_wifi()
    # Sắp xếp theo sóng mạnh nhất
    networks.sort(key=lambda x: x['signal'], reverse=True)
    return {"networks": networks}

@router.post("/connect")
async def connect_wifi(payload: WifiConnectRequest, background_tasks: BackgroundTasks):
    """
    API nhận lệnh kết nối.
    Sau khi trả về response OK cho client, server sẽ tự reboot sau 5s.
    """
    # Gửi lệnh reboot vào background để API kịp trả lời Client "OK" trước khi sập
    background_tasks.add_task(handle_connection_and_reboot, payload.ssid, payload.password)
    return {"status": "connecting", "message": "Thiết bị đang kết nối và sẽ khởi động lại trong 10s..."}

async def handle_connection_and_reboot(ssid, password):
    """Hàm chạy ngầm: Kết nối wifi -> Đợi -> Reboot"""
    print(f"🔄 Đang thử kết nối vào {ssid}...")
    success = network_service.connect_wifi(ssid, password)
    
    if success:
        print("✅ Kết nối lệnh gửi thành công. Đợi 5s để reboot...")
        await asyncio.sleep(5)
        network_service.reboot_system()
    else:
        print("❌ Lỗi: Không thể gửi lệnh kết nối nmcli.")