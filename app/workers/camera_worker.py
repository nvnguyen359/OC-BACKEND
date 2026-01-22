# app/workers/camera_worker.py

# =============================================================================
# FACADE MODULE
# File này map lại các thành phần đã tách để giữ tương thích với code cũ.
# Các module khác vẫn có thể gọi: 
# from app.workers.camera_worker import camera_system, CameraRuntime
# =============================================================================

# 1. Import các hằng số/hàm tiện ích nếu cần thiết (từ camera_runtime)
from app.workers.camera_runtime import (
    CameraRuntime,
    FPS_RECORD
)

# 2. Import System quản lý và instance singleton (từ camera_system)
from app.workers.camera_system import (
    CameraSystem, 
    camera_system
)

# Bây giờ, bất kỳ file nào gọi "import camera_worker" sẽ tự động
# nhận được các class và biến từ 2 file con mới tách ra.