from typing import List, TYPE_CHECKING
from sqlmodel import Field, Session, SQLModel, Relationship
from ..models.user_project import UserProjectLink

if TYPE_CHECKING:
    from ..models.user import User

class Project(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field()
    description: str  = Field()
    url: str = Field()
    created_at: str = Field(default="2023-10-01T00:00:00Z")
    updated_at: str = Field(default="2023-10-01T00:00:00Z") 

    users_link: List["UserProjectLink"] = Relationship(back_populates="project")
    users: List["User"] = Relationship(
        back_populates="projects", link_model=UserProjectLink
    )