from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
import enum

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: PriorityEnum = PriorityEnum.medium

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    owner_id: int
    
   

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[date] = None
    priority: Optional[PriorityEnum] = None

    class Config:
        from_attributes = True