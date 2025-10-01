from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    metric_type = Column(String)  # one_rm, endurance, volume, etc.
    value = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    user = relationship("User", back_populates="performance_metrics")
    exercise = relationship("Exercise", back_populates="performance_metrics")