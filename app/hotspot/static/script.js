/* app/hotspot/script.js */
function showMsg(msg, type='error') {
    const el = document.getElementById('msgBox');
    el.style.display = 'block';
    el.innerHTML = msg;
    el.style.background = type === 'error' ? '#fee2e2' : '#d1fae5';
    el.style.color = type === 'error' ? '#991b1b' : '#065f46';
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('tab-' + tab).classList.add('active');
}

async function scanWifi() {
    const btn = document.getElementById('btnScan');
    const list = document.getElementById('wifiList');
    btn.innerHTML = '<span class="spinner"></span> Đang quét...';
    btn.disabled = true;
    list.style.display = 'none';

    try {
        const res = await fetch('/setup/scan');
        const data = await res.json();
        list.innerHTML = '';
        
        if (data.networks && data.networks.length > 0) {
            data.networks.forEach(net => {
                const li = document.createElement('li');
                li.className = 'wifi-item';
                li.innerHTML = `<span>${net.ssid}</span> <span class="wifi-signal">${net.signal}%</span>`;
                li.onclick = () => {
                    document.getElementById('ssid').value = net.ssid;
                    document.getElementById('password').focus();
                };
                list.appendChild(li);
            });
            list.style.display = 'block';
        } else {
            showMsg('Không tìm thấy mạng wifi nào.');
        }
    } catch (e) {
        showMsg('Lỗi khi quét wifi: ' + e);
    } finally {
        btn.innerHTML = '🔍 Quét Mạng Xung Quanh';
        btn.disabled = false;
    }
}

async function connectWifi() {
    const ssid = document.getElementById('ssid').value;
    const password = document.getElementById('password').value;
    const btn = document.getElementById('btnConnect');

    if (!ssid) return showMsg('Vui lòng chọn hoặc nhập tên Wifi');

    btn.innerHTML = '<span class="spinner"></span> Đang kết nối...';
    btn.disabled = true;

    try {
        const res = await fetch('/setup/connect', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ssid, password})
        });
        const data = await res.json();
        
        if (data.status === 'connecting') {
            showMsg('✅ Đã gửi lệnh kết nối! Thiết bị sẽ khởi động lại trong 10 giây. Vui lòng kết nối điện thoại vào Wifi mới.', 'success');
        } else {
            showMsg('⚠️ ' + data.message);
            btn.disabled = false;
            btn.innerHTML = 'Kết Nối & Khởi Động Lại';
        }
    } catch (e) {
        showMsg('Lỗi gửi lệnh: ' + e);
        btn.disabled = false;
    }
}

async function testCamera() {
    const url = document.getElementById('rtspUrl').value;
    const btn = document.getElementById('btnTestCam');
    const resBox = document.getElementById('camResult');

    if (!url) return showMsg('Nhập link RTSP!');
    
    btn.innerHTML = '<span class="spinner"></span> Đang thử Ping Camera...';
    btn.disabled = true;
    resBox.innerHTML = '';

    try {
        const res = await fetch('/setup/test-camera', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({rtsp: url})
        });
        const data = await res.json();
        if (data.ok) {
            resBox.innerHTML = `<span style="color:green">✅ Kết nối thành công! Size: ${data.width}x${data.height}</span>`;
        } else {
            resBox.innerHTML = `<span style="color:red">❌ Không thể kết nối: ${data.error}</span>`;
        }
    } catch (e) {
        resBox.innerHTML = `<span style="color:red">❌ Lỗi API: ${e}</span>`;
    } finally {
        btn.innerHTML = 'Kiểm Tra Kết Nối';
        btn.disabled = false;
    }
}