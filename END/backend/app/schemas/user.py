from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    login: str
    role: str = "guest"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponse(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str