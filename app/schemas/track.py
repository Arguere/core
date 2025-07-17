from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class TrackBase(BaseModel):
    title: str

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    id: UUID4
    user_id: UUID4
    
    class Config:
        from_attributes = True