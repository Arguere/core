from pydantic import BaseModel
from typing import Optional

class MethodBase(BaseModel):
    title: str
    description: Optional[str] = None
    tutorial: Optional[str] = None

class MethodCreate(MethodBase):
    learning_path_id: int

class Method(MethodBase):
    id: int
    learning_path_id: int
    
    class Config:
        orm_mode = True