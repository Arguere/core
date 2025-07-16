from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TrackBase(BaseModel):
    title: str
    objectives: Optional[str] = None

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True