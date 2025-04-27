from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from ..database import get_session as get_db
from ..schemas.auth_schemas import LoginRequest, TokenResponse
from ..schemas.user_schemas import UserResponse, UserCreate
from ..services.auth_services import AuthService
from ..repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter(tags=["auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)):
    """Obtiene el servicio de autenticación con sus dependencias"""
    repository = UserRepository(db)
    service = AuthService(repository)
    return service


@router.post("/login")
async def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user = service.login(credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = service.create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=120))
        return TokenResponse(access_token=access_token, 
                             token_type="bearer", 
                             user_id=user.id,
                             user_email=user.email)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/register")
async def register(
    user:UserCreate,
    service: AuthService = Depends(get_auth_service)
)->UserResponse:
    try:
        newUser = service.register(user.model_dump())
    except Exception as e:
        raise e
    return newUser
    
@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme), service: AuthService = Depends(get_auth_service))->UserResponse:
    try:
        user = service.get_current_user(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))