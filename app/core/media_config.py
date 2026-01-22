# app/core/media_config.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.session import SessionLocal
from app.db.models import Setting

DEFAULT_MEDIA_FOLDER = "OC-media"

def configure_static_media(app: FastAPI):
    """
    Đọc cấu hình 'save_media' từ DB và mount thư mục tĩnh.
    """
    media_path = DEFAULT_MEDIA_FOLDER
    
    # 1. Lấy đường dẫn từ Database
    try:
        db = SessionLocal()
        # Tìm setting theo key='save_media'
        setting = db.query(Setting).filter(Setting.key == "save_media").first()
        
        if setting and setting.value and setting.value.strip():
            media_path = setting.value.strip()
        
        db.close()
    except Exception as e:
        print(f"⚠️ [Startup] Warning loading media setting: {e}. Using default '{media_path}'")

    # 2. Tạo folder vật lý nếu chưa có
    if not os.path.exists(media_path):
        try:
            os.makedirs(media_path, exist_ok=True)
            print(f"📂 [Startup] Created media folder: {media_path}")
        except Exception as e:
            print(f"❌ [Startup] Error creating folder: {e}")

    # 3. Mount Static Files
    # URL: http://domain.com/{media_path}/filename.jpg
    try:
        app.mount(f"/{media_path}", StaticFiles(directory=media_path), name="media")
        print(f"✅ [Startup] Mounted Media: '/{media_path}' -> './{media_path}'")
    except Exception as e:
        print(f"❌ [Startup] Mount Error: {e}")