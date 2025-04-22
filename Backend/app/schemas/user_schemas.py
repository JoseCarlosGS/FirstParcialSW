from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]

class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str
    last_login: Optional[str] = None
    is_superuser: Optional[bool] = False
    class Config:
        orm_mode = True