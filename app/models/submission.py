from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    content_type = Column(String)  # 'audio' or 'text'
    speech_rate = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    spectral_clarity = Column(Float, nullable=True)
    asr_accuracy = Column(Float, nullable=True)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="submissions")
    scenario = relationship("Scenario", back_populates="submissions")
    feedback = relationship("Feedback", back_populates="submission")