from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import datetime

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User") 