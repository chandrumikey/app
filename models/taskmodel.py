from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base  # your declarative_base

import enum

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date, nullable=True)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="tasks")  # Make sure your User model has tasks relationship
