from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ops = "ops"
    client = "client"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_verified: bool

    class Config:
        orm_mode = True 