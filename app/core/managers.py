from collections import defaultdict
from typing import Dict, Set, Any

from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = defaultdict(set)

    async def connect(self, chat_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[chat_id].add(websocket)

    async def disconnect(self, chat_id: int, websocket: WebSocket) -> None:
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def send_message(self, chat_id: int, message_data: dict[str, Any]) -> None:
        for connection in self.active_connections[chat_id]:
            await connection.send_json(message_data)
