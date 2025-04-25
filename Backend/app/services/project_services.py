from typing import Optional, List
import os
import uuid
from fastapi import UploadFile
from pathlib import Path
import shutil
import json

from ..repositories.project_repository import ProjectRepository
from ..repositories.user_repository import UserRepository
from ..models.project import Project
from ..models.user import User
from ..models.user_project import UserProjectLink
from fastapi import HTTPException

class ProjectService:
    
    def __init__(self, project_repository: ProjectRepository, user_repository: UserRepository ):
        self.user_repo = user_repository
        self.project_repo = project_repository
        
    def create_project(self, data: dict, user_id: int, file: UploadFile ) -> UserProjectLink:
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail={"detail":"user not found"})
            path = self._save_project_file(file)
            data["url"] = path
            project = Project(**data)
            project = self.project_repo.create_project(project)
            return self.project_repo.add_user_to_project(user_id=user.id, project_id=project.id, is_owner=True)
        except ValueError as e:
            raise e
        
    def update_project(self, project_id:int, file:UploadFile ) ->Project:
        try:
            project = self.project_repo.get_project_by_id(project_id)
            if not project:
                raise HTTPException(status_code=404, detail={"detail":"Project not found"})
            self._update_project_file(project.url, file)
            return project
            
        except ValueError as e:
            raise e
        
    def load_project_by_id(self, project_id: int):
        try:
            project = self.project_repo.get_project_by_id(project_id)
            if not project:
                raise HTTPException(status_code=404, detail={"detail":"Project not found"})
            url = project.url
            return self._load_project_file(url) 
        except ValueError as e:
            raise e
        
    def add_user_to_project(self, user_id: int, project_id: int)-> UserProjectLink:
        try:
            user = self.user_repo.get_user_by_id(user_id)
            project = self.project_repo.get_project_by_id(project_id)
            if not user or not project:
                raise HTTPException(status_code=404, detail={"detail":"user or project not found"})
            return self.project_repo.add_user_to_project(user_id=user.id, project_id=project.id, is_owner=False)
        except ValueError as e:
            raise e
        
    def get_all_by_user_id(self, user_id:int)->List[dict]:
        if not self.user_repo.get_user_by_id(user_id):
            raise HTTPException(status_code=404, detail={"detail":"user not found"}) 
        return self.project_repo.get_projects_by_user(user_id)
        
    def get_users_by_project(self, project_id:int)->List[User]:
        if not self.project_repo.get_project_by_id(project_id):
            return HTTPException(status_code=404, detail={"detail":"project not found"})
        return self.project_repo.get_users_by_project(project_id)
    
    def remove_user_from_project(self, user_id:int, project_id:int)->bool:
        try:
            return self.project_repo.deactivate_user_in_project(user_id, project_id)        
        except ValueError as e:
            raise e
        
    def _save_project_file(self, file: UploadFile) -> str:
        # Crear carpeta si no existe
        save_dir = Path("saved_projects")
        save_dir.mkdir(parents=True, exist_ok=True)

        # Generar un ID único y crear el nombre del archivo
        unique_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix or ".json"
        file_name = f"{unique_id}{file_extension}"
        file_path = save_dir / file_name

        # Guardar el archivo en disco
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Devolver ruta relativa o absoluta si lo prefieres
        return str(file_path)
    
    def _load_project_file(self, file_path: str):
        """
        Carga un archivo JSON desde la ruta especificada y devuelve su contenido como un diccionario.
        
        :param file_path: Ruta al archivo JSON (relativa o absoluta).
        :return: Contenido del archivo como un diccionario.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"El archivo {file_path} no existe.")
        
        return path
    
    def _update_project_file(self, file_path: str, file: UploadFile)-> str:
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return file_path
        except Exception as e:
            raise ValueError(f"No se pudo actualizar el archivo en {file_path}. Error: {str(e)}")