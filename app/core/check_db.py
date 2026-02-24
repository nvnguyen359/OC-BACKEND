# app/core/check_db.py
import sys
import os
from passlib.hash import argon2
from sqlalchemy import inspect

# --- 1. CẤU HÌNH ĐƯỜNG DẪN CHUẨN (FIX PATH) ---
# Mục đích: Giúp Python tìm thấy thư mục 'app' dù bạn chạy file này ở đâu
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../app/core
app_dir = os.path.dirname(current_dir)                 # .../app
project_root = os.path.dirname(app_dir)                # .../ (Project Root)

# Thêm thư mục gốc dự án vào sys.path để import được 'app.*'
if project_root not in sys.path:
    sys.path.append(project_root)

# --- 2. IMPORTS ---
from app.core.config import settings
from app.db.session import engine, SessionLocal

# [FIX QUAN TRỌNG] 
# Import module models để đảm bảo code trong đó được chạy và đăng ký bảng
import app.db.models 

# [FIX LOGIC] 
# Thay vì import Base từ db.base, ta lấy Base TRỰC TIẾP từ module models.
# Điều này đảm bảo ta đang dùng đúng đối tượng Base đã chứa User, Camera...
target_metadata = app.db.models.Base.metadata

def init_db_tables():
    """
    Tự động kiểm tra và tạo bảng nếu chưa tồn tại.
    """
    print(f"⏳ Đang kiểm tra Database tại: {settings.DB_URL}")
    
    # [DEBUG] In ra danh sách các bảng mà Code tìm thấy trong bộ nhớ
    detected_models = list(target_metadata.tables.keys())
    print(f"👀 Models đã nạp vào bộ nhớ (Python): {detected_models}")
    
    if not detected_models:
        print("❌ LỖI: Danh sách Model rỗng! Có lỗi import trong file models.py")
        return

    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # 1. Tự động tạo bảng mới
        print("🔨 Đang thực thi lệnh tạo bảng (create_all)...")
        target_metadata.create_all(bind=engine)
        
        # Kiểm tra lại DB thực tế
        inspector = inspect(engine)
        current_tables = inspector.get_table_names()
        
        print(f"✅ Các bảng hiện có trong DB thực tế: {current_tables}")

        new_tables = [t for t in current_tables if t not in existing_tables]
        
        if new_tables:
            print(f"🎉 Đã tạo mới các bảng: {', '.join(new_tables)}")
        elif current_tables:
            print(f"✅ Database đã sẵn sàng.")
        else:
            print("❌ LỖI NGHIÊM TRỌNG: Database vẫn rỗng! Kiểm tra lại quyền ghi file (Permission).")

    except Exception as e:
        print(f"❌ Lỗi khi đồng bộ cấu trúc Database: {e}")

def ensure_admin_user():
    """
    Kiểm tra và khởi tạo user admin mặc định
    """
    db = SessionLocal()
    try:
        # Import lại User từ models
        from app.db.models import User
        
        # Check bảng users có tồn tại không trước khi query
        inspector = inspect(engine)
        if "users" not in inspector.get_table_names():
            print("⚠️ Bảng 'users' chưa được tạo. Bỏ qua bước tạo admin.")
            return

        admin_exists = db.query(User).first()
        if not admin_exists:
            print("⚡ Bảng users rỗng, đang tạo user admin mặc định...")
            try:
                password_hash = argon2.hash("123456") 
                new_admin = User(
                    username="admin",
                    password_hash=password_hash,
                    full_name="Administrator",
                    role="admin",
                    is_active=1
                )
                db.add(new_admin)
                db.commit()
                print("✅ Tài khoản 'admin' (pass: 123456) đã được tạo thành công.")
            except Exception as create_err:
                print(f"❌ Không thể tạo admin: {create_err}")
                db.rollback()
        else:
            print("✅ Tài khoản Admin đã tồn tại.")

    except Exception as e:
        print(f"⚠️ Lỗi khi khởi tạo dữ liệu mẫu: {e}")
    finally:
        db.close()

def main():
    print("==========================================")
    print("      DATABASE CHECK & INITIALIZATION     ")
    print("==========================================")
    init_db_tables()
    ensure_admin_user()
    print("==========================================")

if __name__ == "__main__":
    main()