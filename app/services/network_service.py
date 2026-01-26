# app/services/network_service.py
import subprocess
import platform
import time
import logging

logger = logging.getLogger("network")

class NetworkService:
    def __init__(self):
        self.os_type = platform.system() # 'Windows' hoặc 'Linux'
        # Trên Orange Pi 3 LTS, interface wifi thường là wlan0. 
        # Nếu dùng USB Wifi ngoài, có thể là wlx... cần kiểm tra bằng 'ip a'
        self.interface = "wlan0" 

    def _run_command(self, command):
        """Hàm wrapper chạy lệnh shell an toàn"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Chỉ log warning để tránh spam log khi scan không thấy mạng
            logger.warning(f"Command failed: {command} | Error: {e.stderr.strip()}")
            return None

    def check_internet(self):
        """
        Kiểm tra mạng bằng cách ping Google DNS (8.8.8.8).
        Timeout cực ngắn (1s) để boot nhanh.
        """
        if self.os_type == "Windows":
            return True # [DEV] Windows luôn giả định có mạng
        
        # Ping 1 gói, timeout 1 giây
        cmd = "ping -c 1 -W 1 8.8.8.8"
        return self._run_command(cmd) is not None

    def scan_wifi(self):
        """Quét Wifi xung quanh"""
        if self.os_type == "Windows":
            return [
                {"ssid": "Wifi_Test_1", "signal": 90, "security": "WPA2"},
                {"ssid": "Wifi_Test_2", "signal": 50, "security": "WPA2"}
            ]

        # nmcli: -t (terse/gọn), -f (fields)
        cmd = "nmcli -t -f SSID,SIGNAL,SECURITY dev wifi list"
        output = self._run_command(cmd)
        
        networks = []
        seen_ssids = set()
        
        if output:
            for line in output.split('\n'):
                # Định dạng nmcli -t dùng dấu : hoặc \: để escape
                # Xử lý đơn giản bằng split(':')
                parts = line.split(':')
                if len(parts) >= 2:
                    ssid = parts[0]
                    # Bỏ qua SSID rỗng hoặc trùng lặp
                    if not ssid or ssid in seen_ssids:
                        continue
                    
                    try:
                        signal = int(parts[1]) if parts[1].isdigit() else 0
                        security = parts[2] if len(parts) > 2 else ""
                        
                        networks.append({
                            "ssid": ssid,
                            "signal": signal,
                            "security": security
                        })
                        seen_ssids.add(ssid)
                    except: pass
        return networks

    def connect_wifi(self, ssid, password):
        """Kết nối Wifi mới"""
        logger.info(f"Connecting to Wifi: {ssid}...")
        
        if self.os_type == "Windows":
            time.sleep(1)
            return True

        # 1. Xóa profile cũ để tránh lỗi conflict UUID
        self._run_command(f"nmcli connection delete id '{ssid}'")
        
        # 2. Kết nối
        cmd = f"nmcli dev wifi connect '{ssid}' password '{password}'"
        result = self._run_command(cmd)
        return result is not None

    def enable_hotspot(self, ssid="ORDER_CAMERA_SETUP", password="admin_camera"):
        """
        Bật Hotspot để người dùng kết nối vào cấu hình.
        Đây là 'Phao cứu sinh' khi mất mạng.
        """
        logger.info(f"Enabling Hotspot: {ssid}")
        
        if self.os_type == "Windows":
            return True

        # 1. Ngắt kết nối hiện tại để giải phóng card wifi
        self._run_command(f"nmcli dev disconnect {self.interface}")
        
        # 2. Xóa kết nối Hotspot cũ (nếu có)
        self._run_command(f"nmcli connection delete id '{ssid}'")

        # 3. Tạo Hotspot mới (Mode ap - Access Point)
        # ipv4.method shared: Giúp cấp DHCP cho client kết nối vào
        cmd = (
            f"nmcli con add type wifi ifname {self.interface} con-name '{ssid}' "
            f"autoconnect yes ssid '{ssid}' "
            f"802-11-wireless.mode ap 802-11-wireless.band bg "
            f"ipv4.method shared "
            f"wifi-sec.key-mgmt wpa-psk wifi-sec.psk '{password}'"
        )
        if self._run_command(cmd):
            # Kích hoạt connection vừa tạo
            return self._run_command(f"nmcli con up '{ssid}'") is not None
        return False

    def reboot_system(self):
        """Reboot sau khi cấu hình xong"""
        if self.os_type != "Windows":
            self._run_command("reboot")

network_service = NetworkService()