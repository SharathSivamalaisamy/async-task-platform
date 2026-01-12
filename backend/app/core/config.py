from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Async Task Platform"
    environment: str = "development"
    debug: bool = True

    database_url: str = "postgresql://postgres:postgres@db:5432/tasks_db"

    class Config:
        env_file = ".env"


settings = Settings()
