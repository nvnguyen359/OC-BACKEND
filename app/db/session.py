from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# [LƯU Ý QUAN TRỌNG]
# Kiểm tra lại file config.py xem bạn đặt tên biến là DATABASE_URL hay DB_URL
# Code dưới đây dùng settings.DATABASE_URL theo chuẩn chung.
db_url = getattr(settings, "DATABASE_URL", getattr(settings, "DB_URL", "sqlite:///./sql_app.db"))

# Tạo Engine
engine = create_engine(
    db_url,
    # check_same_thread=False: Bắt buộc để SQLite chạy được nhiều luồng (Web + Camera)
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
    pool_pre_ping=True,
)

# --- [NÂNG CẤP] KÍCH HOẠT CHẾ ĐỘ WAL (Write-Ahead Logging) ---
# Tác dụng:
# 1. Cho phép vừa Đọc (Web) vừa Ghi (Camera) cùng lúc -> Web không bị đơ.
# 2. Tăng tốc độ truy vấn lên gấp 5-10 lần.
# 3. Giảm nguy cơ lỗi "Database is locked".
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in db_url:
        cursor = dbapi_connection.cursor()
        # Chế độ ghi nhật ký song song (Quan trọng nhất)
        cursor.execute("PRAGMA journal_mode=WAL")
        # Giảm bớt việc đồng bộ ổ cứng để tăng tốc (Vẫn an toàn)
        cursor.execute("PRAGMA synchronous=NORMAL")
        # Tăng bộ nhớ đệm lên ~64MB để đọc nhanh hơn
        cursor.execute("PRAGMA cache_size=-64000")
        # Chờ tối đa 5s nếu DB bị khóa (Tránh lỗi ngay lập tức)
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()

# Tạo Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()