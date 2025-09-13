from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
class UserLogin(BaseModel):
    email:  EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
    class Config:
        from_attributes = True