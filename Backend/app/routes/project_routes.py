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
from ..schemas.user_schemas import UserResponse

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

@router.get("/projects")
async def get_all(user_id: int,
                  service: ProjectService = Depends(get_project_service))->list[ProjectResponse]:
    return service.get_all_by_user_id(user_id)


    

@router.get("/users")
async def get_users(project_id: int,
                  service: ProjectService = Depends(get_project_service))->list[UserResponse]:
    return service.get_users_by_project(project_id)


@router.post("/{user_id}")
async def create_project(
    user_id: int,
    project: ProjectRequest = Depends(ProjectRequest.as_form),
    file: UploadFile = File(...),
    service: ProjectService = Depends(get_project_service),
):
    try:
        new_project = service.create_project(project.model_dump(), user_id, file)
        return new_project
    except Exception as e:
        raise HTTPException(status_code=400, detail={"detail": str(e)})


@router.put("/{project_id}")
async def update_project(
    project_id: int,
    file: UploadFile = File(...),
    service: ProjectService = Depends(get_project_service),
):
    try:
        updated_project = service.update_project(project_id, file)
        return updated_project
    except Exception as e:
        raise HTTPException(status_code=400, detail={"detail": str(e)})

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
    
@router.get("/load")
async def load_project(
    project_id: int, 
    service: ProjectService=Depends(get_project_service)):
    json_path = service.load_project_by_id(project_id)
    return FileResponse(
        json_path,
        media_type="application/zip",
        filename=f"angular-project-{project_id}.zip"
    )
    
@router.patch("/add")
async def add_user_to_project(
    user_id:int,
    project_id: int, 
    service: ProjectService=Depends(get_project_service)
):
    return service.add_user_to_project(user_id, project_id)

@router.patch("/remove")
async def remove_user_to_project(
    user_id:int,
    project_id: int, 
    service: ProjectService=Depends(get_project_service)
):
    return service.remove_user_from_project(user_id, project_id)


@router.get("/{project_id}")
async def get_by_id(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
    )->ProjectResponse:
    return service.ger_project_by_id(project_id)