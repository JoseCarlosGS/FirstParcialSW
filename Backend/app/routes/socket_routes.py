from datetime import datetime
import json
import uuid
from fastapi import APIRouter, Depends, WebSocketDisconnect, WebSocket
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from ..database import get_session as get_db

from ..services.socket_services import ConnectionManager, message_history

router = APIRouter(prefix="/socket", tags=["sockets"])

manager = ConnectionManager()

def get_connection_manager():
    return manager

#manager = ConnectionManager()

@router.get("/")
async def get():
    return HTMLResponse("html")

editor_states = {} 

@router.websocket("/ws/{client_id}/{username}")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: str, 
    username: str,
    db: Session = Depends(get_db)):
    
    # Usar la misma instancia del ConnectionManager para todos los clientes
    manager = get_connection_manager()
    await manager.connect(websocket, client_id, username, db)
    
    if editor_states:
        # Obtener el estado más reciente (de cualquier cliente)
        latest_state = next(iter(editor_states.values()))
        await websocket.send_json({
            "type": "editor-state",
            "data": latest_state
        })
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            
            if message_type == "chat-message":
                # Mensaje de chat
                new_message = {
                    "id": str(uuid.uuid4()),
                    "userId": client_id,
                    "text": message_data["text"],
                    "timestamp": datetime.now().isoformat()
                }
                message_history.append(new_message)
                if len(message_history) > 100:
                    message_history.pop(0)
                
                await manager.broadcast(json.dumps({
                    "type": "message",
                    "data": new_message
                }))
            
            elif message_type == "editor-update":
                editor_data = message_data.get("data")
                
                # Si es una sincronización completa, actualizar el estado almacenado
                if editor_data.get("action") == "full-sync":
                    editor_states[client_id] = {
                        "pages": editor_data.get("pages", []),
                        "activePageIndex": editor_data.get("activePageIndex", 0)
                    }
                
                # Broadcast de la actualización
                await manager.broadcast_except_sender(json.dumps({
                    "type": "editor-update",
                    "data": editor_data,
                    "userId": client_id
                }), sender_id=client_id)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast_user_list()