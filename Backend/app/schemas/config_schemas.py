from pydantic import BaseModel, Field

class ProjectConfig(BaseModel):
    project_name: str
    routing: bool = False
    style: str = "css"
    skip_git: bool = True