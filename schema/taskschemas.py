from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    user_id: int

class TaskResponse(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
