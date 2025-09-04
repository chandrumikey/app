from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: str



class UserCreate(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
