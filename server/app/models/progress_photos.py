from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.database import Base

class ProgressPhoto(Base):
    __tablename__ = "progress_photos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photo_url = Column(String)
    photo_type = Column(String)  # front, side, back
    notes = Column(String, nullable=True)
    measurements = Column(JSON, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="progress_photos")