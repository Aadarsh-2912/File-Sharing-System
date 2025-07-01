from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.utils.database import Base

class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expiry = Column(DateTime) 