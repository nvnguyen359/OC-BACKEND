#!/bin/bash
set -e

echo "=================================================="
echo "🚀 CÀI ĐẶT HỆ THỐNG AUTO CAMERA (NORMAL MODE)"
echo "=================================================="

# 1. CÀI ĐẶT PHẦN MỀM HỆ THỐNG
echo "🔄 [1/5] Cài đặt System Dependencies..."
sudo apt-get update
sudo apt-get install -y ffmpeg libzbar0 libgl1-mesa-glx libglib2.0-0 python3-dev build-essential pkg-config libatlas-base-dev gfortran

# 2. TẠO CẤU TRÚC THƯ MỤC (OC-media thật)
echo "📂 [2/5] Tạo thư mục lưu trữ OC-media..."
# Tạo thư mục ngay tại thư mục gốc (ngang hàng với app)
mkdir -p OC-media/avatars
mkdir -p OC-media/videos
mkdir -p OC-media/temp_rec

# Cấp quyền ghi thoải mái (777) để Code và Web đều đọc/ghi được
chmod -R 777 OC-media
echo "✅ Đã tạo folder: $(pwd)/OC-media"

# 3. THIẾT LẬP MÔI TRƯỜNG VENV
echo "🐍 [3/5] Cài đặt môi trường ảo Python..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# 4. CÀI ĐẶT THƯ VIỆN (Thứ tự quan trọng để không bị lỗi sập nguồn)
echo "📦 [4/5] Cài đặt thư viện..."

# --- FIX LỖI CHIP ORANGE PI (QUAN TRỌNG) ---
echo "🔧 Cài Numpy 1.23.5 (Bản ổn định cho Orange Pi 3)..."
pip install "numpy==1.23.5"

echo "🔥 Cài PyTorch CPU..."
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu

echo "👁️ Cài OpenCV & YOLO..."
# Dùng bản headless để nhẹ hệ thống
pip install "opencv-python-headless==4.8.0.76" "ultralytics==8.0.200"

echo "📚 Cài các thư viện còn lại..."
pip install -r requirements.txt

# 5. TẠO FILE CHẠY & SERVICE
echo "⚙️ [5/5] Cấu hình khởi động..."

# Tạo file run.sh
cat > run.sh <<EOL
#!/bin/bash
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
cd "\$DIR"

# Cấu hình môi trường (Fix lỗi CPU & Cache)
export OPENBLAS_CORETYPE=ARMV8
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

if [ ! -d "venv" ]; then
    echo "❌ Lỗi: Chưa có venv!"
    exit 1
fi

source venv/bin/activate
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
EOL
chmod +x run.sh

# Tạo Service
SERVICE_FILE="/etc/systemd/system/autocamera.service"
CURRENT_DIR=$(pwd)

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Auto Camera AI System
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/run.sh
Environment=OPENBLAS_CORETYPE=ARMV8
Environment=PYTHONDONTWRITEBYTECODE=1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable autocamera.service

echo "=================================================="
echo "✅ CÀI ĐẶT HOÀN TẤT!"
echo "👉 Thư mục data: $(pwd)/OC-media"
echo "👉 Hãy chạy lệnh: sudo systemctl restart autocamera.service"
echo "=================================================="