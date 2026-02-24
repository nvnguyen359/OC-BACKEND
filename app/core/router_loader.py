# app/core/router_loader.py
import pkgutil
import importlib
import traceback
from fastapi import FastAPI
from app.api import routers

def auto_include_routers(app: FastAPI):
    package_path = routers.__path__ 
    package_name = routers.__name__ 

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        if module_name.startswith("__"):
            continue

        try:
            module = importlib.import_module(f"{package_name}.{module_name}")

            if hasattr(module, "router"):
                # THÊM PREFIX /api ĐỂ KHÔNG XUNG ĐỘT VỚI FRONTEND SPA
                app.include_router(module.router, prefix="/api")
                
                # Cập nhật log
                actual_prefix = module.router.prefix if module.router.prefix else "/api"
                print(f"✅ Đã load router: {module_name:15} -> {actual_prefix}")
            else:
                print(f"⚠️ Bỏ qua {module_name}: Không tìm thấy biến 'router'")
                
        except Exception as e:
            print(f"❌ Lỗi khi load router {module_name}: {e}")
            traceback.print_exc() # Thêm dòng này để in chi tiết lỗi (call stack)