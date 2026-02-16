# app/crud/setting_crud.py
from sqlalchemy.orm import Session
from app.db.models import Setting

class SettingCRUD:
    def get_all_as_dict(self, db: Session) -> dict:
        """Lấy tất cả cấu hình, ưu tiên giá trị trong DB so với mặc định"""
        settings_list = db.query(Setting).all()
        result = {}
        
        # Danh sách cấu hình mặc định tối ưu cho Orange Pi 3
        defaults = {
            "save_media": "OC-media",
            "camera_width": "854",
            "camera_height": "480",
            "ai_confidence": "0.5",
            "timeout_no_human": "60",
            "work_end_time": "18:30",
            "read_end_order": "5",
            "perf_record_fps": "10.0",
            "perf_view_fps": "15.0",
            "perf_ai_interval": "12",
            "enable_audio": "false"
        }
        
        # Gán giá trị mặc định
        result.update(defaults)
        
        # Ghi đè bằng dữ liệu thực trong DB nếu tồn tại
        for item in settings_list:
            if item.key and item.value:
                result[item.key] = item.value
                
        return result

    def get_value(self, db: Session, key: str) -> str:
        """Lấy giá trị của một key cụ thể"""
        item = db.query(Setting).filter(Setting.key == key).first()
        return item.value if item else None

    def update_batch(self, db: Session, settings_dict: dict):
        """
        Cập nhật nhiều cấu hình cùng lúc.
        Đã fix: Đảm bảo commit đúng cách và thêm log để debug
        """
        try:
            print(f"📥 [Settings] Đang xử lý lưu {len(settings_dict)} mục cấu hình...")
            
            for key, value in settings_dict.items():
                # Chuyển mọi giá trị sang string để lưu vào DB (Cột value thường là String)
                val_str = str(value) if value is not None else ""
                
                existing = db.query(Setting).filter(Setting.key == key).first()
                
                if existing:
                    # Chỉ cập nhật nếu giá trị thực sự thay đổi để tối ưu DB
                    if existing.value != val_str:
                        existing.value = val_str
                        print(f"  🔄 Update: {key} = {val_str}")
                else:
                    # Tạo mới nếu key chưa tồn tại trong DB
                    new_setting = Setting(key=key, value=val_str)
                    db.add(new_setting)
                    print(f"  🆕 Create: {key} = {val_str}")
            
            # Lưu thay đổi vào Database
            db.commit()
            print("✅ [Settings] Lưu cấu hình thành công!")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"❌ [Settings] Lỗi khi lưu cấu hình: {str(e)}")
            return False

setting = SettingCRUD()