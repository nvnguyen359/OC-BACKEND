#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# --- KHẮC PHỤC LỖI ILL (QUAN TRỌNG) ---
# Đổi từ CORTEXA53 sang ARMV8 để tương thích tốt hơn với chip H6
export OPENBLAS_CORETYPE=ARMV8

# Các biến môi trường khác giữ nguyên
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Kiểm tra venv
if [ ! -d "venv" ]; then
    echo "❌ Lỗi: Chưa tìm thấy 'venv'!"
    exit 1
fi

echo "🚀 Kích hoạt môi trường ảo..."
source venv/bin/activate

# --- KIỂM TRA NHANH TRƯỚC KHI CHẠY ---
# Thử import thư viện xem có sập không (để biết ngay lỗi)
python -c "import numpy; import torch; print('✅ Thư viện Toán học OK')"

echo "🔥 Đang khởi động Camera AI System..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1