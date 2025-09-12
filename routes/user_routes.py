# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.models.usermodel import User as UserMaster
# import app.crud.usercrud as usercrud
# from fastapi.security import OAuth2PasswordRequestForm         
# from app.schema.userschema import UserCreate, UserResponse
# from app.core.database import get_db
# from fastapi import FastAPI, Depends, HTTPException
# from app.schema.userschema import Token
# from app.core.auth import verify_password, create_access_token, get_password_hash

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.post("/signup", response_model=UserResponse)
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = usercrud.get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     new_user = usercrud.create_user(db, user)
#     return new_user


# # @router.post("/create/", response_model=UserResponse)
# # def create_user(user: UserCreate, db: Session = Depends(get_db)):
# #     return usercrud.create_user(db=db, user=user)

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(UserMaster).filter(UserMaster.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/", response_model=list[UserResponse])
# def read_users(db: Session = Depends(get_db)):
#     return usercrud.get_users(db)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schema.userschema import UserCreate, UserResponse, Token
from app.crud import usercrud
from app.core.database import get_db
from app.core.auth import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

# Signup
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = usercrud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return usercrud.create_user(db, user)

# Login
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = usercrud.get_user_by_email(db, form_data.username)
    if not user or user.hashed_password != form_data.password:   # 🔑 simple compare
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Protected route
@router.get("/me")
def get_me(token: str = Depends(create_access_token)):
    return {"msg": "You are logged in!", "token": token}

