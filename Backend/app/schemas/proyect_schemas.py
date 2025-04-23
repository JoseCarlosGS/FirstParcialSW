from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class ProjectSchema(BaseModel):
    name: str
    description: str
    
class ProjectRequest(ProjectSchema):
    url: Optional[str] = None
    
    @classmethod
    def as_form(cls, name: str = Form(...), description: str = Form(...)):
        return cls(name=name, description=description)
    
class ProjectResponse(ProjectSchema):
    id: int
    created_at: str
    updated_at: str