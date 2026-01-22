-- db/migrations/init.sql

-- 1. Bảng USERS
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'operator',
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng CAMERAS
CREATE TABLE IF NOT EXISTS cameras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    unique_id TEXT UNIQUE NOT NULL,
    device_id TEXT UNIQUE NOT NULL,
    display_name TEXT,
    rtsp_url TEXT,
    backend TEXT,
    prefer_gst INTEGER DEFAULT 0,
    is_connected INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    device_path TEXT,
    os_index INTEGER DEFAULT 0
);

-- 3. Bảng ORDERS
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_id INTEGER,
    user_id INTEGER,
    parent_id INTEGER,
    session_id TEXT,
    code TEXT,
    status TEXT DEFAULT 'packing',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    start_at DATETIME,
    closed_at DATETIME,
    path_avatar TEXT,
    path_video TEXT,
    order_metadata TEXT,
    note TEXT,
    
    -- Khóa ngoại: Giữ lại đơn hàng (SET NULL) nếu Camera/User bị xóa
    FOREIGN KEY(camera_id) REFERENCES cameras(id) ON DELETE SET NULL,
    FOREIGN KEY(parent_id) REFERENCES orders(id) ON DELETE SET NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 4. Bảng SETTINGS (Đã sửa cú pháp cho SQLite)
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Trigger tự động cập nhật thời gian cho bảng settings (Mô phỏng ON UPDATE CURRENT_TIMESTAMP)
CREATE TRIGGER IF NOT EXISTS update_settings_timestamp 
AFTER UPDATE ON settings
BEGIN
    UPDATE settings SET updated_at = CURRENT_TIMESTAMP WHERE id = new.id;
END;