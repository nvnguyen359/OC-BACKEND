# app/workers/camera_worker.py

# =============================================================================
# FACADE MODULE
# File này map lại các thành phần đã tách để giữ tương thích với code cũ.
# Các module khác vẫn có thể gọi: 
# from app.workers.camera_worker import camera_system, CameraRuntime
# =============================================================================

# 1. Import class chính
# [FIX] Đã bỏ FPS_RECORD ở đây vì bên runtime không còn dùng hằng số này nữa
from app.workers.camera_runtime import CameraRuntime

# 2. Import System quản lý và instance singleton (từ camera_system)
from app.workers.camera_system import (
    CameraSystem, 
    camera_system
)

# Export rõ ràng để các module khác import không bị lỗi
__all__ = ["CameraRuntime", "CameraSystem", "camera_system"]