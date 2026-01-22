# app/services/socket_service.py
import asyncio
import json
from typing import List
from fastapi import WebSocket

class SocketService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.loop = None

    def set_loop(self, loop):
        """
        Lưu Event Loop chính của FastAPI. 
        Cần gọi hàm này ở sự kiện 'startup' trong main.py để có thể gửi tin từ thread khác.
        """
        self.loop = loop

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # print(f"🔌 [Socket] Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            # print(f"🔌 [Socket] Client disconnected. Total: {len(self.active_connections)}")

    async def _broadcast_async(self, message: dict):
        """Gửi tin nhắn đến tất cả client đang kết nối (Chạy trong Async Loop)"""
        if not self.active_connections:
            return
            
        txt = json.dumps(message, default=str)
        # Tạo bản sao danh sách để tránh lỗi Runtime nếu list thay đổi khi đang gửi
        for connection in list(self.active_connections):
            try:
                await connection.send_text(txt)
            except Exception:
                self.disconnect(connection)

    def broadcast_event(self, event_type: str, data: dict):
        """
        Hàm này Thread-Safe, có thể gọi từ Camera Thread (Synchronous).
        Nó sẽ đẩy task gửi tin nhắn vào Event Loop chính của Server.
        """
        if self.loop and self.active_connections:
            payload = {"event": event_type, "payload": data}
            asyncio.run_coroutine_threadsafe(self._broadcast_async(payload), self.loop)

# Singleton Instance
socket_service = SocketService()