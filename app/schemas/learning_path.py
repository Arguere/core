from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LearningPathBase(BaseModel):
    title: str
    objectives: Optional[str] = None

class LearningPathCreate(LearningPathBase):
    pass

class LearningPath(LearningPathBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True