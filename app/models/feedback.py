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
    
    # Store the complete structured feedback
    structured_feedback = Column(JSONB, nullable=False)  # Full GeneratedFeedback structure
    
    # Keep some key fields at root level for easy querying
    overall_performance = Column(String, nullable=True)  # "Excellent", "Good", "Fair", "Needs Improvement"
    total_score = Column(Integer, nullable=True)  # 0-100 from score_summary
    content_alignment_score = Column(Integer, nullable=True)  # 0-25
    scenario_appropriateness_score = Column(Integer, nullable=True)  # 0-25
    communication_clarity_score = Column(Integer, nullable=True)  # 0-25
    audio_delivery_score = Column(Integer, nullable=True)  # 0-25
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    submission = relationship("Submission", back_populates="feedback")