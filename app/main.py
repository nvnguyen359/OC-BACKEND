# app/main.py
import sys
import os
from pathlib import Path

# Đưa định vị lên đầu để tránh lỗi import
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from contextlib import asynccontextmanager
import uvicorn
import asyncio
import psutil
import signal
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.core.auth_middleware import AuthMiddleware
from app.core.router_loader import auto_include_routers
from app.core.openapi_config import configure_openapi
from app.core.docs_utils import custom_swagger_ui_html_response
from app.core.check_db import main as check_db_main
from app.services.socket_service import socket_service
from app.crud.setting_crud import setting as setting_crud
from app.db.session import SessionLocal
from app.workers.run_worker import start_all_workers, stop_all_workers

os.environ["OPENCV_LOG_LEVEL"] = "OFF"

try:
    print("🛠️ [PRE-BOOT] Checking Database Structure...")
    check_db_main()
except Exception as e:
    print(f"⚠️ [PRE-BOOT] DB Init Warning: {e}")

# =========================================================================
# HỆ THỐNG GIẾT TIẾN TRÌNH RÁC TẬN GỐC (TRÁNH TREO CPU)
# =========================================================================
def kill_process_tree():
    print("🛑 Đang bẻ khóa các luồng AI bị kẹt và giải phóng CPU...")
    try:
        parent = psutil.Process(os.getpid())
        for child in parent.children(recursive=True):
            child.kill()
    except Exception:
        pass
    os._exit(0)

def brutal_kill(*args):
    print("\n⚡ Nhận lệnh tắt (Ctrl+C). Ép hệ thống dừng khẩn cấp!")
    try: stop_all_workers()
    except: pass
    kill_process_tree()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 API Server running at http://{settings.HOST}:{settings.PORT}")
    try: socket_service.set_loop(asyncio.get_running_loop())
    except: pass

    print("🔄 [BOOT] Initializing Background Workers...")
    start_all_workers()

    # Ghi đè handler tắt khẩn cấp
    try:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, brutal_kill)
        loop.add_signal_handler(signal.SIGTERM, brutal_kill)
    except NotImplementedError:
        # Dành riêng cho Windows
        signal.signal(signal.SIGINT, brutal_kill)

    yield  

    print("👋 API Server shutting down...")
    try: stop_all_workers()
    except: pass
    kill_process_tree()

APP_DIR = Path(__file__).resolve().parent
DOCS_DIR = APP_DIR / "docs"
CLIENT_DIR = APP_DIR.parent / "client" / "browser"

app = FastAPI(
    title="Order Camera AI API",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)

auto_include_routers(app)
configure_openapi(app)

try:
    app.mount("/socket.io", socket_service.app)
    print("🔌 [SOCKET] Realtime service mounted at /socket.io")
except Exception:
    pass

# =========================================================================
# [FIX VIDEO & ẢNH] API STREAMING CAO CẤP HỖ TRỢ HTTP 206 CHO VIDEO
# =========================================================================
def send_bytes_range_requests(file_obj, start: int, end: int, chunk_size: int = 1_000_000):
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)

@app.get("/api/OC-media/{file_path:path}")
async def serve_media(file_path: str, request: Request):
    # 1. Tự động xử lý dấu \ của Windows
    clean_path = file_path.replace("\\", "/")
    
    # 2. [SỬA LỖI TÌM SAI THƯ MỤC] Định vị thư mục OC-media ở gốc dự án
    try:
        db = SessionLocal()
        val = setting_crud.get_value(db, "save_media")
        db.close()
        # Đổi mặc định thành "OC-media" thay vì "media"
        real_media_path_str = val if val else "OC-media" 
    except Exception:
        real_media_path_str = "OC-media"

    # Dùng root_dir (thư mục OC-BACkEND) làm mỏ neo thay vì APP_DIR
    if Path(real_media_path_str).is_absolute():
        base_dir = Path(real_media_path_str).resolve()
    else:
        base_dir = (Path(root_dir) / real_media_path_str).resolve()
        
    full_path = (base_dir / clean_path).resolve()

    # 3. Kiểm tra bảo mật & tồn tại
    if not str(full_path).startswith(str(base_dir)):
        return JSONResponse({"error": "Invalid path"}, status_code=400)
        
    if not full_path.exists() or not full_path.is_file():
        print(f"❌ [MEDIA 404] TÌM SAI CHỖ! Đang tìm tại: {full_path}")
        return JSONResponse({"error": "File not found"}, status_code=404)

    # 4. Trả về Ảnh (HTTP 200) hoặc Stream Video (HTTP 206)
    file_size = full_path.stat().st_size
    content_type = "video/mp4" if full_path.suffix.lower() == ".mp4" else "image/jpeg"
    range_header = request.headers.get("range")

    if range_header and content_type == "video/mp4":
        try:
            h = range_header.replace("bytes=", "").split("-")
            start = int(h[0]) if h[0] != "" else 0
            end = int(h[1]) if h[1] != "" else file_size - 1
        except ValueError:
            return JSONResponse({"error": "Invalid range"}, status_code=416)
            
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1),
            "Content-Type": content_type,
        }
        return StreamingResponse(
            send_bytes_range_requests(open(full_path, "rb"), start, end),
            headers=headers,
            status_code=206,
        )
    else:
        return FileResponse(full_path, media_type=content_type)

@app.get("/docs", include_in_schema=False)
async def docs_page():
    return custom_swagger_ui_html_response(
        openapi_url=app.openapi_url, title=app.title, docs_dir=DOCS_DIR
    )

@app.get("/")
async def read_root():
    index_path = CLIENT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not found"}, status_code=404)

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = CLIENT_DIR / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    index_path = CLIENT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not found"}, status_code=404)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)