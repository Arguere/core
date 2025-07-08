from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    what_went_well: str
    suggestions: str

class FeedbackCreate(FeedbackBase):
    submission_id: int

class Feedback(FeedbackBase):
    id: int
    submission_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True