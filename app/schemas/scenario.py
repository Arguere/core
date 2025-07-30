from typing import Dict, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class ScenarioBase(BaseModel): 
    user_id: UUID4


class ScenarioCreate(ScenarioBase):
    context: str
    additional_info: Optional[Dict[str, str]] = None


class Scenario(ScenarioBase):
    id: UUID4 
    title: str
    knowledge_foundation: str
    guideline: Dict[str, str]
    created_at: datetime

    class Config:
        from_attributes = True


class ScenarioResponse(ScenarioBase):
    """Response model that includes both the scenario data and creation context"""
    id: UUID4 
    title: str
    knowledge_foundation: str
    guideline: Dict[str, str]
    created_at: datetime
    
    class Config:
        from_attributes = True