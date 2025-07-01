from pydantic import BaseModel, EmailStr
import enum

class UserRole(str, enum.Enum):
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
        from_attributes = True 