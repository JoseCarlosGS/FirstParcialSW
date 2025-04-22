from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from ..services.utils.password_encoder import hash_password, verify_password


SECRET_KEY = "your_secret_key"  # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"  # Algoritmo de codificación
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, user_data: Dict[str, Any]) -> User:
        """
        Crea un nuevo usuario con los datos proporcionados.
        """
        # Comprobar si el usuario ya existe
        existing_user = self.user_repository.get_user_by_email(user_data.get("email"))
        if existing_user:
            raise ValueError("Ya existe un usuario con ese correo electrónico")
        
        hash = hash_password(user_data["password"])
        user_data["password"] = hash
        # Crear instancia de usuario
        user = User(**user_data)
        
        # Guardar usuario
        return self.user_repository.create_user(user)
    
    def login(self, email: str, password: str) -> Optional[User]:
        """
        Inicia sesión con el correo electrónico y la contraseña proporcionados.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        user.last_login = datetime.now(timezone.utc)
        self.user_repository.update_user(user.id)
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def get_current_user(self, token: str):
        try:
            # Decodifica el token JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials or token has expired: {e}")

        # Busca al usuario en la base de datos
        user = self.user_repository.get_user_by_email(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    