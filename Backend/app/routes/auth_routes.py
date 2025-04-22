from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from ..database import get_session as get_db
from ..schemas.auth_schemas import LoginRequest, TokenResponse
from ..services.auth_services import AuthService
from ..repositories.user_repository import UserRepository

def get_auth_service(db: AsyncSession = Depends(get_db)):
    """Obtiene el servicio de autenticación con sus dependencias"""
    repository = UserRepository(db)
    service = AuthService(repository)
    return service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user = service.login(credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return TokenResponse(access_token=user.access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    