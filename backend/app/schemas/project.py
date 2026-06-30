from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    owner: str
    status: str = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True
