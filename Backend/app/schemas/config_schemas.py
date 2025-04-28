from pydantic import BaseModel, Field

class Page(BaseModel):
    name: str
    html: str
    css: str
    typescript: str

class ProjectConfig(BaseModel):
    project_name: str
    routing: bool = False
    style: str = "css"
    skip_git: bool = True
    standalone: bool = True
    pages : list[Page]