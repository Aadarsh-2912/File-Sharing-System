from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.utils.database import Base
import enum

class UserRole(str, enum.Enum):
    ops = "ops"
    client = "client"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole))
    is_verified = Column(Boolean, default=False) 