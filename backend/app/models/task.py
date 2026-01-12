from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, Text
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
  


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    payload = Column(JSON, nullable=False)
    result = Column(JSON)
    error = Column(Text)

    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
