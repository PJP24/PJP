from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatusEnum(enum.Enum):
    accepted = "accepted"
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_type = Column(String(100), nullable=False)
    status = Column(Enum(TaskStatusEnum), nullable=False)
    result = Column(String(255), nullable=True)
    scheduled_time = Column(DateTime, default=datetime.utcnow)
    completed_time = Column(DateTime, nullable=True)

