from typing import Dict
from pydantic import BaseModel, UUID4, Json
from datetime import datetime


class ScenarioBase(BaseModel): 
    user_id: UUID4
    context: str
    additional_info: Dict[str, str] = None


class ScenarioCreate(ScenarioBase):
    pass

class Scenario(ScenarioBase):
    id: UUID4 
    title: str
    knowledge_foundation: str
    guideline: Dict[str, str]
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True
    
