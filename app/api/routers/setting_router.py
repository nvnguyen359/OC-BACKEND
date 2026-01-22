# app/api/routers/setting_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.api import deps
from app.crud.setting_crud import setting as setting_crud
from app.db.schemas import SettingsUpdate, SettingsResponse

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(deps.get_db)):
    """
    Lấy toàn bộ cấu hình hệ thống.
    Nếu DB chưa có, sẽ trả về giá trị mặc định (save_media, resolution...).
    """
    data = setting_crud.get_all_as_dict(db)
    return {
        "code": 200,
        "mes": "success",
        "data": data
    }

@router.post("/", response_model=SettingsResponse)
def update_settings(
    payload: Dict[str, Any], # Nhận trực tiếp JSON {key: value}
    db: Session = Depends(deps.get_db)
):
    """
    Cập nhật cấu hình (Batch Update).
    Body ví dụ:
    {
        "save_media": "D:/MyData",
        "camera_width": 1920,
        "camera_height": 1080
    }
    """
    success = setting_crud.update_batch(db, payload)
    
    if not success:
        return {
            "code": 500,
            "mes": "Update failed",
            "data": {}
        }

    # Trả về dữ liệu mới nhất sau khi update
    new_data = setting_crud.get_all_as_dict(db)
    return {
        "code": 200,
        "mes": "Settings updated successfully",
        "data": new_data
    }