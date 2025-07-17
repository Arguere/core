from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    content_type: str

class SubmissionCreate(SubmissionBase):
    scenario_id: UUID4

class Submission(SubmissionBase):
    id: UUID4
    user_id: UUID4
    scenario_id: UUID4
    speech_rate: Optional[float] = None
    duration: Optional[float] = None
    spectral_clarity: Optional[float] = None
    asr_accuracy: Optional[float] = None
    score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True