from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .database import init_db
from .routes import user_routes
from .routes import project_routes
from .routes.project_routes import generator

app = FastAPI(title="Angular Project Generator API")

@app.on_event("startup")
def on_startup():
    init_db()
    
app.include_router( user_routes.router, prefix="/api")
app.include_router( project_routes.router, prefix="/api")    

@app.websocket("/ws/project/{project_id}")
async def project_status_websocket(websocket: WebSocket, project_id: str):
    await websocket.accept()
    
    delivery_system = generator.delivery_system
    try:
        await delivery_system.track_project_status(project_id, websocket)
    except WebSocketDisconnect:
        pass
 
@app.get("/")
async def home():
    return {
        "message":"Hello world"
    } 