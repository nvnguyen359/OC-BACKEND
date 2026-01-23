#!/bin/bash

# Lấy đường dẫn thư mục hiện tại
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Kiểm tra xem venv đã có chưa
if [ ! -d "venv" ]; then
    echo "❌ Chưa tìm thấy môi trường ảo. Hãy chạy ./setup.sh trước!"
    exit 1
fi

echo "🚀 Đang khởi động Camera AI System..."
source venv/bin/activate

# Khởi chạy Server với Uvicorn
# --host 0.0.0.0 để có thể truy cập từ máy tính khác trong mạng LAN
# --reload chỉ dùng khi dev, khi chạy thật nên bỏ đi để ổn định
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000