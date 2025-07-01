from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.utils.database import Base
import datetime

class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    expiry = Column(DateTime, default=lambda: datetime.datetime.utcnow()) 