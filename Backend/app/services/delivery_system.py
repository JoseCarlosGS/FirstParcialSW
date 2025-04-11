# delivery_system.py
import os
import json
import shutil
import asyncio
import aiofiles
from fastapi import BackgroundTasks, WebSocket
from typing import Dict, Any, List

class ProjectDeliverySystem:
    def __init__(self):
        self.projects_dir = os.path.join(os.getcwd(), "generated_projects")
        self.status_cache = {}  # Caché de estado de proyectos
    
    async def track_project_status(self, project_id: str, websocket: WebSocket):
        """Envía actualizaciones de estado del proyecto a través de WebSocket"""
        try:
            status_file = os.path.join(self.projects_dir, project_id, "status.json")
            
            while True:
                if os.path.exists(status_file):
                    async with aiofiles.open(status_file, 'r') as f:
                        status = json.loads(await f.read())
                    await websocket.send_json(status)
                    
                    if status["status"] in ["completed", "failed"]:
                        break
                else:
                    await websocket.send_json({"status": "initializing", "progress": 0})
                
                await asyncio.sleep(1)
                
        except Exception as e:
            await websocket.send_json({"status": "error", "message": str(e)})
    
    def update_project_status(self, project_id: str, status: Dict[str, Any]):
        """Actualiza el estado de un proyecto"""
        status_file = os.path.join(self.projects_dir, project_id, "status.json")
        os.makedirs(os.path.dirname(status_file), exist_ok=True)
        
        with open(status_file, 'w') as f:
            json.dump(status, f)
        
        self.status_cache[project_id] = status
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Obtiene el estado actual del proyecto"""
        if project_id in self.status_cache:
            return self.status_cache[project_id]
            
        status_file = os.path.join(self.projects_dir, project_id, "status.json")
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                status = json.load(f)
            self.status_cache[project_id] = status
            return status
        
        return {"status": "unknown"}
    
    def cleanup_old_projects(self, max_age_hours: int = 24):
        """Limpia proyectos antiguos para liberar espacio"""
        import time
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        cutoff_timestamp = cutoff_time.timestamp()
        
        for item in os.listdir(self.projects_dir):
            item_path = os.path.join(self.projects_dir, item)
            if os.path.isdir(item_path):
                mod_time = os.path.getmtime(item_path)
                if mod_time < cutoff_timestamp:
                    shutil.rmtree(item_path, ignore_errors=True)