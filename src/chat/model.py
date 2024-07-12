from typing import List
from fastapi import WebSocket, WebSocketDisconnect

class ChatConnection:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def sendtext(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)

    async def broadcast(self, text: str):
        for connection in self.active_connections:
            await connection.send_text(text)

    

chat = ChatConnection()