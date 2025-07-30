from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import JSONB


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False)
    transcription = Column(String, nullable=True)  # Store the transcription
    audio_metrics = Column(JSONB, nullable=True)  # Store audio analysis metrics
    processing_status = Column(String, default="pending", nullable=False)  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    scenario = relationship("Scenario", back_populates="submissions")
    feedback = relationship("Feedback", back_populates="submission", cascade="all, delete-orphan")