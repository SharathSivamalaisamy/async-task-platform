from fastapi import FastAPI
from app.core.config import settings
from app.api import health, tasks
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# Base.metadata.create_all(bind=engine)

app.include_router(health.router)
app.include_router(tasks.router)
