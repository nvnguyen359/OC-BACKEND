import os
import time
import subprocess
import platform

class NetworkService:
    def __init__(self):
        self.interface = "wlan0"
        self.gateway_ip = "192.168.42.1" 
        # Tự động nhận diện hệ điều hành đang chạy
        self.is_windows = platform.system().lower() == "windows"

    def run_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode().strip()
        except:
            return ""

    def check_internet(self):
        # Điều chỉnh lệnh ping tương thích với từng HĐH
        if self.is_windows:
            return os.system("ping -n 1 -w 2000 8.8.8.8 > nul 2>&1") == 0
        else:
            return os.system("ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1") == 0

    def enable_hotspot(self):
        print("🔥 [NETWORK] Đang bật chế độ Hotspot...")
        
        if self.is_windows:
            print("⚠️ [MOCK WINDOWS] Đã giả lập kích hoạt Hotspot thành công.")
            return True

        # --- LỆNH THỰC TẾ TRÊN DIETPI ---
        os.system("systemctl stop hostapd isc-dhcp-server 2>/dev/null")
        os.system("cp /etc/network/interfaces.hotspot /etc/network/interfaces")
        
        os.system(f"ifdown {self.interface} --force; sleep 1; ifup {self.interface} --force")
        time.sleep(2)
        
        os.system(f"ip link set {self.interface} up")
        os.system(f"ip addr flush dev {self.interface} 2>/dev/null")
        os.system(f"ip addr add {self.gateway_ip}/24 dev {self.interface} 2>/dev/null")
        
        os.system("systemctl start hostapd isc-dhcp-server")
        print("✅ Hotspot (DietPi) đã bật thành công. Đang chờ thiết bị kết nối...")
        return True

    def scan_wifi(self):
        print("🔍 [NETWORK] Đang quét Wifi xung quanh...")
        
        if self.is_windows:
            print("⚠️ [MOCK WINDOWS] Trả về danh sách Wifi giả lập.")
            return [
                {"ssid": "Wifi_Test_1", "signal": -50},
                {"ssid": "Wifi_Test_2", "signal": -75}
            ]

        # --- LỆNH THỰC TẾ TRÊN DIETPI ---
        try:
            os.system(f"ifconfig {self.interface} up")
            scan_output = self.run_cmd(f"iwlist {self.interface} scan")
            
            networks = []
            current_network = {}
            for line in scan_output.split('\n'):
                line = line.strip()
                if line.startswith("Cell"):
                    if current_network and 'ssid' in current_network:
                        networks.append(current_network)
                    current_network = {}
                elif line.startswith("ESSID:"):
                    ssid = line.split('"')[1]
                    if ssid: 
                        current_network['ssid'] = ssid
                elif line.startswith("Quality="):
                    parts = line.split("Signal level=")
                    if len(parts) > 1:
                        signal = int(parts[1].split()[0])
                        current_network['signal'] = signal
            
            if current_network and 'ssid' in current_network:
                networks.append(current_network)
            
            unique_networks = {}
            for net in networks:
                ssid = net['ssid']
                if ssid not in unique_networks or net['signal'] > unique_networks[ssid]['signal']:
                    unique_networks[ssid] = net
                    
            return list(unique_networks.values())
        except Exception as e:
            print(f"❌ Lỗi quét wifi: {e}")
            return []

    def connect_wifi(self, ssid, password):
        print(f"🔗 [NETWORK] Đang cấu hình kết nối tới: '{ssid}'")
        
        if self.is_windows:
            print("⚠️ [MOCK WINDOWS] Giả lập kết nối thành công.")
            time.sleep(2)
            return True

        # --- LỆNH THỰC TẾ TRÊN DIETPI ---
        wpa_config = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=VN

network={{
    ssid="{ssid}"
    psk="{password}"
}}
"""
        try:
            with open("/tmp/wpa_supplicant.conf", "w") as f:
                f.write(wpa_config)
            os.system("cp /tmp/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")
            
            print("⏳ [NETWORK] Đang chuyển sang Client Mode...")
            os.system("systemctl stop hostapd isc-dhcp-server 2>/dev/null")
            os.system("cp /etc/network/interfaces.client /etc/network/interfaces")
            
            os.system(f"ifdown {self.interface} --force; sleep 1; ifup {self.interface} --force")
            
            print("⏳ [NETWORK] Đang xin cấp IP từ Router nhà khách...")
            time.sleep(10)
            ip_check = self.run_cmd(f"ip -4 addr show {self.interface}")
            
            if "inet " in ip_check and "192.168.42.1" not in ip_check:
                print("✅ Kết nối thành công!")
                return True
            else:
                print("❌ Kết nối thất bại (Sai pass hoặc Router không cấp IP).")
                return False
        except Exception as e:
            print(f"❌ Lỗi ghi cấu hình wifi: {e}")
            return False
            
    def reboot_system(self):
        if self.is_windows:
            print("⚠️ [MOCK WINDOWS] Bỏ qua lệnh reboot trên Windows.")
        else:
            os.system("reboot")

network_service = NetworkService()