from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.exceptions import register_exception_handlers
from app.core.config import settings
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.project import router as project_router

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(project_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Enterprise Dev Portal API",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": settings.app_version,
    }
