from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.crud as usercrud
from app.schema.userschema import UserCreate, UserResponse
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return usercrud.create_user(db=db, user=user)

@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return usercrud.get_users(db)

