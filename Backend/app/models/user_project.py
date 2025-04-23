from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .project import Project

class UserProjectLink(SQLModel, table=True):
    id_user: int = Field(foreign_key="user.id", primary_key=True)
    id_project: int = Field(foreign_key="project.id", primary_key=True)
    is_active: bool = Field(default=True)
    is_owner: bool = Field(default=False)
    created_at: str = Field(default="2023-10-01T00:00:00Z")
    updated_at: str = Field(default="2023-10-01T00:00:00Z")
    
    user: Optional["User"] = Relationship(back_populates="projects_link")
    project: Optional["Project"] = Relationship(back_populates="users_link")