#!/bin/bash

# Dừng script nếu gặp lỗi
set -e

echo "🚀 [1/5] Bắt đầu cập nhật hệ thống Orange Pi..."
sudo apt-get update && sudo apt-get upgrade -y

echo "📦 [2/5] Cài đặt các thư viện hệ thống cần thiết (System dependencies)..."
# libgl1: Cần cho OpenCV
# libzbar0: Cần cho Pyzbar đọc mã vạch
# python3-venv: Để tạo môi trường ảo
# mpg123: Để phát âm thanh mp3 (TTS)
# v4l-utils: Công cụ kiểm tra camera
sudo apt-get install -y python3-pip python3-venv libgl1 libgl1-mesa-glx libglib2.0-0 libzbar0 mpg123 v4l-utils

echo "🐍 [3/5] Thiết lập môi trường ảo Python (Virtual Environment)..."
# Xóa môi trường cũ nếu có để cài mới cho sạch
if [ -d "venv" ]; then
    echo "   - Đã tìm thấy venv cũ, đang xóa..."
    rm -rf venv
fi

python3 -m venv venv
echo "   - Đã tạo venv mới."

echo "📥 [4/5] Kích hoạt venv và cài đặt thư viện Python..."
source venv/bin/activate

# Cập nhật pip
pip install --upgrade pip

# Cài đặt từ requirements.txt
# --no-cache-dir giúp tiết kiệm dung lượng thẻ nhớ trên Orange Pi
pip install --no-cache-dir -r requirements.txt

echo "⚙️ [5/5] Cấu hình quyền truy cập Camera..."
# Thêm user hiện tại vào nhóm video để đọc được Camera USB/CSI
sudo usermod -aG video $USER

echo "✅ CÀI ĐẶT HOÀN TẤT!"
echo "👉 Hãy chạy lệnh: './run.sh' để khởi động hệ thống."