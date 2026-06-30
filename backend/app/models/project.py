from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="active")
