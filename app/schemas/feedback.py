from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class Feedback(BaseModel):
    id: UUID4
    submission_id: UUID4
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True