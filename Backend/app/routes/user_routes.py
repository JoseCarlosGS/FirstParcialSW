from fastapi import APIRouter
from ..schemas.user_schemas import UserCreate, UserResponse
from ..database import SessionDep
from ..database import get_session as get_db
from ..repositories.user_repository import UserRepository
from ..services.user_services import UserService
from sqlmodel import Session
from fastapi import Depends, HTTPException

router = APIRouter(prefix="/user", tags=["users"])

async def get_user_service(db: Session = Depends(get_db)):
    """Obtiene el servicio de usuarios con sus dependencias"""
    repository = UserRepository(db)
    service = UserService(repository)
    return service

@router.get("/")
async def get_all(UserService: UserService = Depends(get_user_service)) -> list[UserResponse]:
    return UserService.get_all_users()

@router.post("/")
async def create(
    user: UserCreate, 
    UserService: UserService = Depends(get_user_service))-> UserResponse:
    try:
        user = UserService.create_user(user.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user

@router.get("/get-by-email/{email}")
async def get_by_email(email: str, 
    UserService: UserService = Depends(get_user_service))->UserResponse:
    try:
        user = UserService.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail={"error":"User not found"})
        return user
    except Exception as e:
        raise e