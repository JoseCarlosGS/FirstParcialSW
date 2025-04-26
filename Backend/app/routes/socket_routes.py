from datetime import datetime
import json
import uuid
from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from fastapi.responses import HTMLResponse

from ..services.socket_services import ConnectionManager, message_history

router = APIRouter(prefix="/socket", tags=["sockets"])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/api/socket/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

manager = ConnectionManager()

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws/{user_id}/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, user_email:str):
    print(f"Cliente conectado: {user_email} (ID: {user_id})")
    await manager.connect(websocket, user_id, user_email)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Mensaje recibido de {user_email}: {data}")
            message_data = json.loads(data)
            
            # Crear nuevo mensaje
            new_message = {
                "id": str(uuid.uuid4()),
                "userId": user_id,
                "text": message_data["text"],
                "timestamp": datetime.now().isoformat()
            }
            print(f"Nuevo mensaje creado: {new_message}")
            
            # Guardar en historial
            message_history.append(new_message)
            if len(message_history) > 100:  # Limitar historial a 100 mensajes
                message_history.pop(0)
            
            # Broadcast del mensaje a todos los clientes
            await manager.broadcast(json.dumps({
                "type": "message",
                "data": new_message
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast_user_list()