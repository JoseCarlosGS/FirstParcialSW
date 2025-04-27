import json
from typing import Dict
from fastapi import WebSocket
from ..models.user import User
from ..repositories.user_repository import UserRepository
from sqlmodel import Session


message_history = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.users: Dict[str, dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str, username: str, db: Session):
        await websocket.accept()
        
        # Convertir client_id a string para uso consistente
        client_id = str(client_id)
        self.active_connections[client_id] = websocket
        
        # Obtener datos del usuario
        from ..repositories.user_repository import UserRepository
        repo = UserRepository(db)
        user = repo.get_user_by_id(client_id)
        
        # Guardar información del usuario
        if user:
            self.users[client_id] = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "last_login": user.last_login
            }
        else:
            # Fallback para usuarios no encontrados
            self.users[client_id] = {
                "id": client_id,
                "name": username,
                "email": username
            }
        
        print(f"Usuario conectado: {username} (ID: {client_id})")
        print(f"Usuarios activos: {len(self.active_connections)}")
        
        # Notificar a todos los clientes sobre el nuevo usuario
        await self.broadcast_user_list()
        
        # Enviar el historial de mensajes al nuevo usuario
        await self.send_message_history(client_id)
    
    def disconnect(self, client_id: str):
        client_id = str(client_id)
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.users:
            del self.users[client_id]
        print(f"Usuario desconectado (ID: {client_id})")
        print(f"Usuarios activos: {len(self.active_connections)}")
    
    async def broadcast(self, message: str):
        print(f"Enviando a {len(self.active_connections)} conexiones: {message[:100]}...")
        for connection in self.active_connections.values():
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
    
    async def broadcast_user_list(self):
        user_list = list(self.users.values())
        message = json.dumps({
            "type": "users",
            "data": user_list
        })
        print(f"Enviando lista de usuarios: {message}")
        await self.broadcast(message)
    
    async def send_message_history(self, client_id: str):
        client_id = str(client_id)
        if client_id in self.active_connections:
            message = json.dumps({
                "type": "history",
                "data": message_history
            })
            print(f"Enviando historial de mensajes a {client_id}")
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                print(f"Error al enviar historial: {e}")
