from typing import Optional, List, Dict, Any

from app.models.user import User
from app.repositories.user_repository import UserRepository
from ..services.utils.password_encoder import hash_password, verify_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data: Dict[str, Any]) -> User:
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

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.
        """
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None
        return user    

    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios.
        """
        return self.user_repository.get_all_users()

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Actualiza los datos de un usuario existente.
        """
        # Comprobar si el usuario existe
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            return None
            
        # Si se está actualizando el email, verificar que no exista otro usuario con ese email
        if "email" in user_data and user_data["email"] != existing_user.email:
            user_with_email = self.user_repository.get_user_by_email(user_data["email"])
            if user_with_email and user_with_email.id != user_id:
                raise ValueError("Ya existe otro usuario con ese correo electrónico")
                
        # Actualizar usuario
        return self.user_repository.update_user(user_id, **user_data)

    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario por su ID.
        """
        return self.user_repository.delete_user(user_id)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica un usuario por email y contraseña.
        Nota: Asume que el modelo User tiene un método check_password.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user or not user.check_password(password):
            return None
        return user