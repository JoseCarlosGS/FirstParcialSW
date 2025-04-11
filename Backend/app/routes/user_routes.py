from fastapi import APIRouter
from ..schemas.user_shemas import UserCreate, UserResponse
from ..database import SessionDep

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/")
async def get_all():
    pass

@router.post("/")
async def create(user: UserCreate, session: SessionDep)-> UserCreate:
    session.add(user)
    session.commit() 
    session.refresh(user)
    return user