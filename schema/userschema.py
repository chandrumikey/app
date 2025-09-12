from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(UserBase):
    password: str   # plain password on signup
# class UserCreate(UserBase):
#     hashed_password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attribute = True
