from sqlalchemy.orm import Session
from app.models.usermodel import User
from app.schema.userschema import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
