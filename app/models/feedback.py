from sqlalchemy import Column, UUID, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    score = Column(Float, nullable=True)  # Overall score out of 100
    audio_metrics = Column(JSONB, nullable=True)  # Store audio analysis metrics for reference
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    submission = relationship("Submission", back_populates="feedback")