from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    content_type: str

class SubmissionCreate(SubmissionBase):
    scenario_id: int

class Submission(SubmissionBase):
    id: int
    user_id: int
    scenario_id: int
    speech_rate: Optional[float] = None
    duration: Optional[float] = None
    spectral_clarity: Optional[float] = None
    asr_accuracy: Optional[float] = None
    score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True