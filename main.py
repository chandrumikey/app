from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schema.userschema import UserCreate, UserResponse
from app.schema.taskschemas import TaskCreate, TaskResponse
from app.crud import usercrud, taskcrud

app = FastAPI(title="Prodexa API")

# Users
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return usercrud.create_user(db, user)

@app.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return usercrud.get_users(db)

# Tasks
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return taskcrud.create_task(db, task)

@app.get("/tasks/", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return taskcrud.get_tasks(db)
