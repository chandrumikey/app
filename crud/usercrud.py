from sqlalchemy.orm import Session
from app.models.usermodel import User
from app.schema.userschema import UserCreate
from app.core.auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
         hashed_password=hashed_pw   # ⛔ storing plain password (for demo)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
