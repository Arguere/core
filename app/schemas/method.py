from pydantic import BaseModel, UUID4
from typing import Optional

class MethodBase(BaseModel):
    title: str
    description: Optional[str] = None
    tutorial: Optional[str] = None

class MethodCreate(MethodBase):
    track_id: UUID4

class Method(MethodBase):
    id: UUID4
    track_id: UUID4
    
    class Config:
        from_attributes = True