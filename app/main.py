# app/main.py

import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager # [NEW] Cần thiết cho Lifespan

# ==============================================================================
# [FIX PATH] TỰ ĐỘNG THÊM ROOT VÀO SYS.PATH
# Giúp chạy được cả lệnh: "python app/main.py" mà không lỗi ModuleNotFoundError
# ==============================================================================
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

# --- Import nội bộ ---
from app.core.config import settings
from app.core.auth_middleware import AuthMiddleware
from app.core.router_loader import auto_include_routers
from app.core.openapi_config import configure_openapi
from app.core.docs_utils import custom_swagger_ui_html_response
from app.core.media_config import configure_static_media
from app.core.check_db import main as check_db_main
from app.services.socket_service import socket_service

# [QUAN TRỌNG] Đã xóa dòng import worker ở đây để tránh lỗi Circular Import
# from app.workers.run_worker import ... (DELETE)

# ==========================================
# 1. LIFESPAN (QUẢN LÝ KHỞI ĐỘNG & TẮT)
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Hàm này thay thế cho @app.on_event("startup") và shutdown.
    Giúp tránh cảnh báo DeprecationWarning và lỗi import vòng vo.
    """
    # --- PHẦN STARTUP ---
    print(f"🚀 API Server running at http://{settings.HOST}:{settings.PORT}")
    
    # Gán Event Loop cho Socket Service
    try:
        socket_service.set_loop(asyncio.get_running_loop())
    except: pass

    print("✅ [BOOT] Starting System Modules...")
    
    # 1. Kiểm tra Database & Cấu hình Media
    try:
        check_db_main()
        configure_static_media(app)
    except Exception as e:
        print(f"⚠️ [BOOT] Database/Config Warning: {e}")

    # 2. Load toàn bộ API Routers
    auto_include_routers(app)
    
    # 3. Cấu hình Docs (Swagger UI)
    configure_openapi(app)

    # 4. Bật Worker (Camera, AI...) - [LAZY IMPORT TẠI ĐÂY]
    print("🔄 [BOOT] Initializing Background Workers...")
    try:
        # Import ở đây để phá vỡ vòng lặp import (Circular Dependency)
        from app.workers.run_worker import start_all_workers
        start_all_workers()
    except Exception as e:
        print(f"❌ [BOOT] Worker Start Failed: {e}")

    # --- APP CHẠY TẠI ĐÂY ---
    yield 
    # --- APP DỪNG TẠI ĐÂY ---

    # --- PHẦN SHUTDOWN ---
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

app = FastAPI(
    title="Order Camera AI API",
    version="2.0.0",
    docs_url=None, # Tắt docs mặc định để dùng Custom Swagger
    redoc_url=None,
    lifespan=lifespan # [NEW] Đăng ký hàm lifespan ở trên vào đây
)

# 3. MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

# ==========================================
# 3. SWAGGER UI (Custom)
# ==========================================
@app.get("/docs", include_in_schema=False)
async def docs_page():
    return custom_swagger_ui_html_response(
        openapi_url=app.openapi_url,
        title=app.title,
        docs_dir=DOCS_DIR
    )

if __name__ == "__main__":
    # Reload=True để ổn định khi Dev
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)