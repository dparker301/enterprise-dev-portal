from app.core.config import settings
from app.database import Base, engine
from app.routers.projects import router as projects_router
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(projects_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Enterprise Dev Portal API"}


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": settings.app_version,
    }
