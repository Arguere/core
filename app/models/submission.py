from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenarios.id"), nullable=False)
    content_type = Column(String)  # 'audio' or 'text'
    speech_rate = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    spectral_clarity = Column(Float, nullable=True)
    asr_accuracy = Column(Float, nullable=True)
    score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("Profile", back_populates="submissions")
    scenario = relationship("Scenario", back_populates="submissions")
    feedback = relationship("Feedback", back_populates="submission")