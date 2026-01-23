#corecheck_db.py
import sys
import os
from passlib.hash import argon2
from sqlalchemy import inspect

# --- CẤU HÌNH ĐƯỜNG DẪN HỆ THỐNG ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from app.core.config import settings  # noqa: E402
from app.db.session import engine, SessionLocal  # noqa: E402
from app.db.base import Base  # noqa: E402
# Import toàn bộ models để Base.metadata nhận diện được tất cả các bảng (User, Camera, Order, Setting)

def init_db_tables():
    """
    Tự động kiểm tra và tạo bảng nếu chưa tồn tại.
    Sử dụng metadata.create_all để tự động phát hiện các Class mới trong models.py
    """
    print(f"⏳ Đang kiểm tra Database tại: {settings.DB_URL}")
    try:
        # Lấy danh sách các bảng hiện có trong DB thực tế
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # 1. Tự động tạo bảng mới nếu phát hiện class mới trong models.py
        # Nếu bảng đã có, SQLAlchemy sẽ tự động bỏ qua (không gây lỗi)
        Base.metadata.create_all(bind=engine)
        
        # Kiểm tra xem có bảng nào vừa được tạo mới không
        new_tables = [t for t in Base.metadata.tables.keys() if t not in existing_tables]
        if new_tables:
            print(f"✅ Đã tạo mới các bảng: {', '.join(new_tables)}")
        else:
            print("✅ Cấu trúc các bảng đã sẵn sàng (không có bảng mới).")

    except Exception as e:
        print(f"❌ Lỗi khi đồng bộ cấu trúc Database: {e}")
        sys.exit(1)

def ensure_admin_user():
    """
    Kiểm tra và khởi tạo user admin mặc định nếu bảng users trống
    """
    db = SessionLocal()
    try:
        from app.db.models import User
        admin_exists = db.query(User).first()
        if not admin_exists:
            print("⚡ Bảng users rỗng, đang tạo user admin mặc định...")
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
    except Exception as e:
        print(f"⚠️ Lỗi khi khởi tạo dữ liệu mẫu: {e}")
    finally:
        db.close()

def main():
    # Bước 1: Đồng bộ hóa Table (Tự động phát hiện table mới từ models.py)
    init_db_tables()
    
    # Bước 2: Kiểm tra dữ liệu mặc định
    ensure_admin_user()

if __name__ == "__main__":
    main()