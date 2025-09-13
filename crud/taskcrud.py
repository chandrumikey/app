
from sqlalchemy.orm import Session
from app.schema import userschema 
from app.schema import taskschemas as schemas
from app.models import taskmodel as models
from app.models import usermodel 
from app.core.auth import get_password_hash
from datetime import date
from typing import List, Optional

def create_user(db: Session, user: userschema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id, 
        models.Task.owner_id == user_id
    ).first()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_with_filters(
    db: Session, 
    user_id: int, 
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    due_date: Optional[date] = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(models.Task).filter(models.Task.owner_id == user_id)
    
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if due_date:
        query = query.filter(models.Task.due_date == due_date)
    
    return query.offset(skip).limit(limit).all()