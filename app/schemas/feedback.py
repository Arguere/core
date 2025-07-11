from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Feedback(BaseModel):
    id: int
    submission_id: int
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True