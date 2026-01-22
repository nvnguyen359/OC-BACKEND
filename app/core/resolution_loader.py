# app/core/resolution_loader.py
from app.db.session import SessionLocal
from app.db.models import Setting

# Mặc định phòng hờ
DEFAULT_W = 1280
DEFAULT_H = 720

def get_system_resolution():
    """
    Trả về (width, height) từ bảng settings.
    Key: 'camera_width', 'camera_height'
    """
    w, h = DEFAULT_W, DEFAULT_H
    try:
        db = SessionLocal()
        
        # Lấy Width
        setting_w = db.query(Setting).filter(Setting.key == "camera_width").first()
        if setting_w and setting_w.value:
            w = int(setting_w.value)
            
        # Lấy Height
        setting_h = db.query(Setting).filter(Setting.key == "camera_height").first()
        if setting_h and setting_h.value:
            h = int(setting_h.value)
            
        db.close()
    except Exception as e:
        print(f"⚠️ Resolution Load Error: {e}. Using default {DEFAULT_W}x{DEFAULT_H}")
        
    return w, h