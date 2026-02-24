from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer # <--- Import thêm cái này
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_access_token
from app.crud.user_crud import user_crud
from app.services.network_service import network_service

router = APIRouter(
    prefix="/system",
    tags=["System"]
)

# --- 1. KHAI BÁO OAUTH2 SCHEME (QUAN TRỌNG) ---
# Phải khai báo biến này để Depends sử dụng được
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# --- 2. DEPENDENCY: CHECK QUYỀN ADMIN ---
def get_current_admin(
    token: str = Depends(oauth2_scheme), # <--- SỬA LỖI TẠI ĐÂY (Bỏ dấu ngoặc kép)
    db: Session = Depends(get_db)
):
    # Giải mã Token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    user = user_crud.get_by_username(db, username)
    
    if not user:
        raise HTTPException(status_code=401, detail="User không tồn tại")
    
    # Check quyền Admin
    is_admin = getattr(user, "is_superuser", False) or getattr(user, "role", "").upper() == "ADMIN"
    
    if not is_admin:
        raise HTTPException(status_code=403, detail="Bạn không có quyền Admin")
        
    return user

# --- 3. API ENDPOINTS ---

@router.post("/reboot")
async def reboot_system(current_user = Depends(get_current_admin)):
    try:
        network_service.reboot_system()
        return {"message": "Hệ thống đang khởi động lại..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hotspot/{action}")
async def toggle_hotspot(
    action: str,
    current_user = Depends(get_current_admin)
):
    if action not in ["on", "off"]:
        raise HTTPException(status_code=400, detail="Action phải là 'on' hoặc 'off'")

    try:
        msg = network_service.toggle_hotspot(action)
        return {"message": msg, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

@router.get("/wifi/scan")
async def scan_wifi(current_user = Depends(get_current_admin)):
    return network_service.scan_wifi()