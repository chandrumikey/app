from sqlalchemy.orm import Session
from app.models.usermodel import User
from app.schema.userschema import UserCreate
from app.core.auth import get_password_hash
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt  
from app.core.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.schema import userschema as schemas
from app.core.database import get_db
from app.crud import usercrud as crud

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

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.UserResponse = Depends(get_current_user)):
    return current_user