# app/crud/setting_crud.py
from sqlalchemy.orm import Session
from app.db.models import Setting

class SettingCRUD:
    def get_all_as_dict(self, db: Session) -> dict:
        settings_list = db.query(Setting).all()
        result = {}
        
        # [CẬP NHẬT] Thêm các key cấu hình mới
        defaults = {
            "save_media": "OC-media",
            "camera_width": "1280",
            "camera_height": "720",
            "ai_confidence": "0.5",
            "timeout_no_human": "60",   # [MỚI] Mặc định 60 giây
            "work_end_time": "18:30",
            "read_end_order":5
        }
        
        result.update(defaults)
        
        for item in settings_list:
            if item.key and item.value:
                result[item.key] = item.value
                
        return result

    def update_batch(self, db: Session, settings_dict: dict):
        try:
            for key, value in settings_dict.items():
                existing = db.query(Setting).filter(Setting.key == key).first()
                val_str = str(value)
                
                if existing:
                    existing.value = val_str
                else:
                    new_setting = Setting(key=key, value=val_str)
                    db.add(new_setting)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"❌ Setting Update Error: {e}")
            return False

setting = SettingCRUD()