from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()
metadata = Base.metadata

class TaskStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_type = Column(String(100), nullable=False)
    status = Column(Enum(TaskStatusEnum), nullable=False)

