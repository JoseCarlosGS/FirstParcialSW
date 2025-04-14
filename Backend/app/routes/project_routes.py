import os
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from ..database import SessionDep
from ..schemas.proyect_schemas import ProjectSchema
from ..schemas.config_schemas import ProjectConfig
from ..schemas.proyect_schemas import print_structure
from ..services.project_generator import AngularProjectGenerator

router = APIRouter(prefix="/project", tags=["projects"])

generator = AngularProjectGenerator()

def borrar_archivo(path: str):
    if os.path.exists(path):
        os.remove(path)

@router.get("/")
async def get_all():
    pass

@router.post("/")
async def create(project: ProjectSchema) -> dict:
    # Para depuración
    
    # Serializar explícitamente para asegurar que todos los campos están presentes
    return project.dict()

@router.post("/alt")
async def create_alt(project: ProjectSchema) -> ProjectSchema:
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