from pydantic import BaseModel
from typing import Optional

class MethodBase(BaseModel):
    title: str
    description: Optional[str] = None
    tutorial: Optional[str] = None

class MethodCreate(MethodBase):
    track_id: int

class Method(MethodBase):
    id: int
    track_id: int
    
    class Config:
        from_attributes = True