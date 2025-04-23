import os
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from ..database import get_session as get_db
from sqlmodel import Session
from ..schemas.proyect_schemas import ProjectRequest, ProjectResponse
from ..schemas.config_schemas import ProjectConfig
from ..services.project_generator import AngularProjectGenerator
from ..repositories.project_repository import ProjectRepository
from ..repositories.user_repository import UserRepository
from ..services.project_services import ProjectService

router = APIRouter(prefix="/project", tags=["projects"])

generator = AngularProjectGenerator()

async def get_project_service(db: Session = Depends(get_db)):
    """Obtiene el servicio de usuarios con sus dependencias"""
    project_repo = ProjectRepository(db)
    user_repo = UserRepository(db)
    service = ProjectService(project_repository=project_repo, user_repository=user_repo)
    return service

def borrar_archivo(path: str):
    if os.path.exists(path):
        os.remove(path)

@router.get("/")
async def get_all():
    pass

@router.post("/{user_id}")
async def create_project(
    user_id: int,
    project: ProjectRequest = Depends(ProjectRequest.as_form),
    file: UploadFile = File(...),
    service: ProjectService = Depends(get_project_service)
):
    try:
        new_project = service.create_project(project.model_dump(), user_id, file)
        return new_project
    except ValueError as e:
        raise HTTPException(status_code=500, detail={"detail": str(e)})

@router.post("/alt")
async def create_alt(project: ProjectRequest) -> ProjectResponse:
    # Para Pydantic v1
    # project_dict = project.dict(by_alias=True, exclude_none=False)
    # Para Pydantic v2
    # project_dict = project.model_dump(by_alias=True, exclude_none=False)
    
    # Luego reconstruir el modelo (esto fuerza una serialización completa)
    # return ProjectSchema(**project_dict)
    
    # O simplemente devolver el proyecto directamente si los cambios de modelo
    # son suficientes
    return project

@router.post("/generate")
async def generate_angular_project(project: ProjectConfig, background_tasks: BackgroundTasks):
    """
    Genera un proyecto Angular basado en el esquema proporcionado.
    Devuelve un token para descargar el proyecto más tarde.
    """
    project_id = str(uuid.uuid4())
    resp = generator.generate_project(project, project_id)
    zip_path = resp.get("zip_path")
    zip_filename = resp.get("zip_filename")
    background_tasks.add_task(borrar_archivo, zip_path)
    #background_tasks.add_task(generator.generate_project, project)
    return FileResponse(zip_path, media_type="application/zip", filename=zip_filename)

@router.post("/component")
async def generate_component(prompt: str, background_tasks: BackgroundTasks):
    """
    Genera un componente Angular basado en el esquema proporcionado.
    Devuelve un token para descargar el componente más tarde.
    """
    project_id = str(uuid.uuid4())
    zip_path = generator.generate_component(prompt=prompt)
    background_tasks.add_task(borrar_archivo, zip_path)
    return FileResponse(path=zip_path, filename="registro_usuario.zip", media_type='application/zip')

@router.get("/download/{project_id}")
async def download_project(project_id: str):
    """Descarga un proyecto generado previamente"""
    zip_path = os.path.join(generator.projects_dir, f"{project_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    return FileResponse(
        zip_path, 
        media_type="application/zip",
        filename=f"angular-project-{project_id}.zip"
    )