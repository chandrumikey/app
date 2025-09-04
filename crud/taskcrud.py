from sqlalchemy.orm import Session
from app.models.taskmodel import Task
from app.schema.taskschemas import TaskCreate

def create_task(db: Session, task: TaskCreate):
    db_task = Task(title=task.title, description=task.description, user_id=task.user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(Task).all()
