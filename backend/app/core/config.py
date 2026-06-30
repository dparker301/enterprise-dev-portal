from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Enterprise Dev Portal"
    app_version: str = "0.1.0"
    environment: str = "local"


settings = Settings()
