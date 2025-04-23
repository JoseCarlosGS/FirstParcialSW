from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING
from ..models.user_project import UserProjectLink

if TYPE_CHECKING:
    from ..models.project import Project
    
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(index=True)
    name: str = Field()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: str = Field(default="2023-10-01T00:00:00Z")
    updated_at: str = Field(default="2023-10-01T00:00:00Z")
    last_login: str = Field(default="2023-10-01T00:00:00Z")
    
    projects_link: List["UserProjectLink"] = Relationship(back_populates="user")
    projects: List["Project"] = Relationship(
        back_populates="users", link_model=UserProjectLink
    )
    
    