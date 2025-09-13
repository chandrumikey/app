# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordBearer
# from app.core.database import get_db
# from app.models.usermodel import User
# from app.schema import taskschemas 
# from app.schema import userschema
# from app.core.security import get_current_user  
# import app.models.usermodel as models
# from app.crud import taskcrud
# from app.core import auth

# router = APIRouter()

# @router.post("/tasks", response_model=taskschemas.TaskOut)
# def create_task(task: taskschemas.TaskCreate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
#     return taskcrud.create_task(db, task, current_user.id)

# @router.get("/tasks", response_model=list[taskschemas.TaskOut])
# def get_tasks(db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
#     return taskcrud.get_tasks(db, current_user.id)

# @router.get("/tasks/{task_id}", response_model=taskschemas.TaskOut)
# def get_task(task_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
#     task = taskcrud.get_task(db, task_id, current_user.id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task

# @router.put("/tasks/{task_id}", response_model=taskschemas.TaskOut)
# def update_task(task_id: int, task: taskschemas.TaskUpdate, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
#     updated = taskcrud.update_task(db, task_id, task, current_user.id)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Task not found or not yours")
#     return updated

# @router.delete("/tasks/{task_id}")
# def delete_task(task_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.get_current_user)):
#     deleted = taskcrud.delete_task(db, task_id, current_user.id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Task not found or not yours")
#     return {"msg": "Task deleted"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date


from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.dependencies.dependencies import get_task_or_404
from app.models import usermodel as User
from app.models import taskmodel as Task
from app.schema import taskschemas as schemas
from app.crud import taskcrud as crud


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.create_user_task(db=db, task=task, user_id=current_user.id)

@router.get("", response_model=List[schemas.TaskResponse])
def read_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    due_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    tasks = crud.get_tasks_with_filters(
        db, 
        user_id=current_user.id,
        completed=completed,
        priority=priority,
        due_date=due_date,
        skip=skip, 
        limit=limit
    )
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def read_task(task: Task = Depends(get_task_or_404)):
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_update: schemas.TaskUpdate,
    task: Task = Depends(get_task_or_404),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.update_task(db=db, task_id=task.id, task_update=task_update, user_id=current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task: Task = Depends(get_task_or_404),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    crud.delete_task(db=db, task_id=task.id, user_id=current_user.id)
    return None