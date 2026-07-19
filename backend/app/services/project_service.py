from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    project_data: ProjectCreate,
    owner_id: int,
) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
        owner_id=owner_id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def list_projects(
    db: Session,
    owner_id: int,
) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .order_by(Project.id)
        .all()
    )


def get_project(
    db: Session,
    project_id: int,
    owner_id: int,
) -> Project | None:
    return (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == owner_id,
        )
        .first()
    )


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
) -> Project:
    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project,
) -> None:
    db.delete(project)
    db.commit()
