from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Dict, Any, Optional

class FeedbackBase(BaseModel):
    submission_id: UUID4
    content: str
    score: Optional[float] = Field(default=None, ge=0, le=100, description="Overall score out of 100")
    audio_metrics: Optional[Dict[str, Any]] = Field(default=None, description="Audio analysis metrics")

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

class DetailedFeedback(BaseModel):
    """Detailed feedback response including all metrics and analysis"""
    id: UUID4
    submission_id: UUID4
    content: str
    score: Optional[float]
    audio_metrics: Optional[Dict[str, Any]]
    transcription: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True