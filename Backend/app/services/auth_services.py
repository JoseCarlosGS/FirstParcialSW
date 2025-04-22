from typing import Optional, List, Dict, Any

from app.models.user import User
from app.repositories.user_repository import UserRepository
from ..services.utils.password_encoder import hash_password, verify_password

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
        return user
    
    