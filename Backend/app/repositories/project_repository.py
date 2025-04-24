from sqlmodel import Session, select

from app.models.project import Project
from app.models.user_project import UserProjectLink
from app.models.user import User

class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_project(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get_project_by_id(self, project_id: int) -> Project | None:
        return self.session.get(Project, project_id)

    def get_all_projects(self) -> list[Project]:
        statement = select(Project)
        return self.session.exec(statement).all()

    def update_project(self, project_id: int, **kwargs) -> Project | None:
        project = self.get_project_by_id(project_id)
        if not project:
            return None
        for key, value in kwargs.items():
            setattr(project, key, value)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def delete_project(self, project_id: int) -> bool:
        project = self.get_project_by_id(project_id)
        if not project:
            return False
        self.session.delete(project)
        self.session.commit()
        return True

    def add_user_to_project(self, user_id: int, project_id: int, is_owner: bool = False) -> UserProjectLink:
        link = UserProjectLink(id_user=user_id, id_project=project_id, is_owner=is_owner)
        self.session.add(link)
        self.session.commit()
        self.session.refresh(link)
        return link

    def remove_user_from_project(self, user_id: int, project_id: int) -> bool:
        statement = select(UserProjectLink).where(
            UserProjectLink.id_user == user_id,
            UserProjectLink.id_project == project_id
        )
        link = self.session.exec(statement).first()
        if not link:
            return False
        self.session.delete(link)
        self.session.commit()
        return True

    def deactivate_user_in_project(self, user_id: int, project_id: int) -> bool:
        statement = select(UserProjectLink).where(
            UserProjectLink.id_user == user_id,
            UserProjectLink.id_project == project_id
        )
        link = self.session.exec(statement).first()
        if not link:
            return False
        link.is_active = False
        self.session.add(link)
        self.session.commit()
        return True

    def get_users_by_project(self, project_id: int) -> list[User]:
        statement = select(User).join(UserProjectLink).where(
            UserProjectLink.id_project == project_id,
            UserProjectLink.is_active == True
        )
        return self.session.exec(statement).all()

    def get_projects_by_user(self, user_id: int) -> list[dict]:
        statement = select(Project, UserProjectLink.is_owner).join(UserProjectLink).where(
            UserProjectLink.id_user == user_id,
            UserProjectLink.is_active == True
        )
        results = self.session.exec(statement).all()
        formatted_results = [
            {
                **project.model_dump(),  # Convierte el objeto Project a un diccionario
                "is_owner": is_owner  # Añade el atributo is_owner como una clave adicional
            }
            for project, is_owner in results
        ]
        return formatted_results
