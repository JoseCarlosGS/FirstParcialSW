import json
from typing import Dict
from fastapi import WebSocket

message_history = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.users: Dict[str, dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str, username: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.users[client_id] = {"name": username, "id": client_id}
        
        # Notificar a todos los clientes sobre el nuevo usuario
        await self.broadcast_user_list()
        
        # Enviar el historial de mensajes al nuevo usuario
        await self.send_message_history(client_id)
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.users:
            del self.users[client_id]
        
    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
    
    async def broadcast_user_list(self):
        user_list = list(self.users.values())
        for connection in self.active_connections.values():
            await connection.send_text(json.dumps({
                "type": "users",
                "data": user_list
            }))
    
    async def send_message_history(self, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(json.dumps({
                "type": "history",
                "data": message_history
            }))
