from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils.database import Base

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    upload_time = Column(DateTime, default=datetime.utcnow)
    user = relationship("User") 