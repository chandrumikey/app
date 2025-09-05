from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud.taskcrud as taskcrud  # your CRUD operations
from app.schema.taskschemas import TaskCreate, TaskResponse   # your Pydantic models
from app.core.database import get_db                   # your DB session dependency

# Create router
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create Task
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return taskcrud.create_task(db=db, task=task)

# Read All Tasks
@router.get("/", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return taskcrud.get_tasks(db)
