from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional, Dict, Any

class SubmissionCreate(BaseModel):
    scenario_id: UUID4
    audio_url: str = Field(..., description="Cloudflare R2 URL to the audio file")

class SubmissionUpdate(BaseModel):
    transcription: Optional[str] = None
    audio_metrics: Optional[Dict[str, Any]] = None
    processing_status: Optional[str] = None

class Submission(BaseModel):
    id: UUID4
    scenario_id: UUID4
    transcription: Optional[str] = None
    audio_metrics: Optional[Dict[str, Any]] = None
    processing_status: Optional[str] = Field(default="pending", description="processing, completed, failed")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config: 
        from_attributes = True

class SubmissionWithFeedback(Submission):
    """Submission with associated feedback"""
    feedback: Optional[Dict[str, Any]] = None