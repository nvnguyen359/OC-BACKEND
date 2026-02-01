# app/api/routers/setting_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.api import deps
from app.crud.setting_crud import setting as setting_crud
from app.db.schemas import SettingsUpdate, SettingsResponse

# [NEW] Import biến global camera_system để kích hoạt hot-reload
from app.workers.camera_system import camera_system

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(deps.get_db)):
    """
    Lấy toàn bộ cấu hình hệ thống.
    """
    data = setting_crud.get_all_as_dict(db)
    return {
        "code": 200,
        "mes": "success",
        "data": data
    }

@router.post("/", response_model=SettingsResponse)
def update_settings(
    payload: Dict[str, Any], 
    db: Session = Depends(deps.get_db)
):
    """
    Cập nhật cấu hình và Hot-Reload hệ thống Camera ngay lập tức.
    """
    success = setting_crud.update_batch(db, payload)
    
    if not success:
        return {
            "code": 500,
            "mes": "Update failed",
            "data": {}
        }

    # [NEW] Kích hoạt Hot-Reload: Bắt các camera đọc lại cấu hình mới
    try:
        camera_system.reload_settings()
    except Exception as e:
        print(f"⚠️ [Settings] Hot-reload trigger failed: {e}")

    # Trả về dữ liệu mới nhất sau khi update
    new_data = setting_crud.get_all_as_dict(db)
    return {
        "code": 200,
        "mes": "Settings updated & System reloaded successfully",
        "data": new_data
    }