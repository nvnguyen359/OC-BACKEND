# app/main.py
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# [FIX PATH] Thêm thư mục gốc vào sys.path
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

# --- Import nội bộ ---
from app.core.config import settings
from app.core.auth_middleware import AuthMiddleware
from app.core.router_loader import auto_include_routers
from app.core.openapi_config import configure_openapi
from app.core.docs_utils import custom_swagger_ui_html_response
from app.core.check_db import main as check_db_main
from app.services.socket_service import socket_service
from app.crud.setting_crud import setting as setting_crud
from app.db.session import SessionLocal

# [FIX 1] Đã xóa import 'configure_static_media' gây lỗi.

# ==========================================
# 1. LIFESPAN
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 API Server running at http://{settings.HOST}:{settings.PORT}")
    try:
        # Thiết lập loop cho socket
        socket_service.set_loop(asyncio.get_running_loop())
    except: pass

    print("✅ [BOOT] Starting System Modules...")
    try:
        check_db_main()
    except Exception as e:
        print(f"⚠️ [BOOT] Database Warning: {e}")

    print("🔄 [BOOT] Initializing Background Workers...")
    try:
        from app.workers.run_worker import start_all_workers
        start_all_workers()
    except Exception as e:
        print(f"❌ [BOOT] Worker Start Failed: {e}")

    yield 

    print("👋 API Server shutting down...")
    try:
        from app.workers.run_worker import stop_all_workers
        stop_all_workers()
    except: pass


# ==========================================
# 2. KHỞI TẠO APP
# ==========================================
APP_DIR = Path(__file__).resolve().parent
DOCS_DIR = APP_DIR / "docs"
# Đường dẫn tới thư mục build Angular
CLIENT_DIR = APP_DIR.parent / "client" / "browser"

app = FastAPI(
    title="Order Camera AI API",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# ==========================================
# 3. LOAD ROUTERS
# ==========================================
auto_include_routers(app)
configure_openapi(app)


# ==========================================
# 4. MOUNT SOCKET.IO (FIX LỖI MẤT REALTIME)
# ==========================================
try:
    # Mount socket app vào đường dẫn /socket.io
    # socket_service.app chính là instance của socketio.ASGIApp
    app.mount("/socket.io", socket_service.app)
    print("🔌 [SOCKET] Realtime service mounted at /socket.io")
except Exception as e:
    print(f"❌ Socket Mount Error: {e}")


# ==========================================
# 5. MOUNT MEDIA THỦ CÔNG (FIX LỖI ẢNH)
# ==========================================
try:
    db = SessionLocal()
    # Lấy đường dẫn lưu ảnh từ DB
    real_media_path_str = setting_crud.get_value(db, "save_media") or "app/media"
    db.close()
    
    real_media_path = Path(real_media_path_str).resolve()
    
    if not real_media_path.exists():
        print(f"📁 Creating media folder: {real_media_path}")
        real_media_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 [MOUNT] URL '/OC-media' -> Real Path '{real_media_path}'")
    
    # Mount cứng đường dẫn ảnh
    app.mount("/OC-media", StaticFiles(directory=real_media_path), name="media")
    
except Exception as e:
    print(f"❌ Media Mount Error: {e}")


# ==========================================
# 6. SWAGGER UI
# ==========================================
@app.get("/docs", include_in_schema=False)
async def docs_page():
    return custom_swagger_ui_html_response(
        openapi_url=app.openapi_url, title=app.title, docs_dir=DOCS_DIR
    )


# ==========================================
# 7. SERVE FRONTEND (FIX LỖI F5 & CATCH-ALL)
# ==========================================
@app.get("/")
async def read_root():
    index_path = CLIENT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not found"}, status_code=404)

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # 1. Tìm file thực tế (js, css, ico...)
    file_path = CLIENT_DIR / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)

    # 2. Nếu không tìm thấy file -> Trả về index.html (Angular tự xử lý)
    index_path = CLIENT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    return JSONResponse({"error": "Frontend not found"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)