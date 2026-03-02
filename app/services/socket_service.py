# app/services/socket_service.py
import socketio
import asyncio


class SocketService:
    def __init__(self):
        # 1. Khởi tạo Async Socket.IO Server
        # cors_allowed_origins='*' để cho phép Angular kết nối từ port khác (vd 4200)
        self.sio = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins="*",
            logger=False,
            engineio_logger=False,
            ping_timeout=60,  # Tăng từ 5s lên 60s để cho máy chủ thở
            ping_interval=25,
        )

        # 2. Tạo ASGI App (Wrapper)
        # socketio_path="" vì bên main.py ta đã mount vào đường dẫn "/socket.io" rồi.
        # Nếu để mặc định nó sẽ thành /socket.io/socket.io -> Client không nối được.
        self.app = socketio.ASGIApp(self.sio, socketio_path="")

        self.loop = None

    def set_loop(self, loop):
        """
        Lưu Event Loop chính của FastAPI.
        Cần gọi hàm này ở sự kiện 'startup' (lifespan) trong main.py.
        """
        self.loop = loop

    def broadcast_event(self, event_type: str, data: dict):
        """
        Hàm gửi sự kiện xuống tất cả client (Thread-Safe).
        Có thể gọi từ luồng Camera (Synchronous) mà không bị lỗi Async.
        """
        if self.loop:
            # Chuyển việc gửi tin nhắn vào luồng chính (Main Loop)
            # Emit trực tiếp event_type (vd: 'ORDER_CREATED') thay vì bọc trong JSON
            coro = self.sio.emit(event_type, data)
            asyncio.run_coroutine_threadsafe(coro, self.loop)
        else:
            print(f"⚠️ [Socket] Event Loop not set. Cannot emit: {event_type}")


# Singleton Instance
socket_service = SocketService()
