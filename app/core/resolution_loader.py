# app/core/resolution_loader.py
from app.db.session import SessionLocal
from app.crud.setting_crud import setting as setting_crud

def get_system_resolution():
    """
    Lấy độ phân giải từ Database.
    Nếu DB chưa cài, dùng mặc định tối ưu cho Orange Pi (854x480).
    """
    db = SessionLocal()
    try:
        # Lấy setting, nếu không có thì trả về None
        w_str = setting_crud.get_value(db, "camera_width")
        h_str = setting_crud.get_value(db, "camera_height")
        
        # Nếu có trong DB thì dùng, không thì dùng mặc định 854x480
        if w_str and h_str:
            return int(w_str), int(h_str)
        else:
            return 854, 480
    except Exception as e:
        print(f"⚠️ Load Resolution Error: {e}, using default.")
        return 854, 480
    finally:
        db.close()