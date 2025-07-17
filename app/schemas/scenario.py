from pydantic import BaseModel, UUID4
from typing import Optional

class ScenarioBase(BaseModel):
    title: str
    description: Optional[str] = None

class ScenarioCreate(ScenarioBase):
    method_id: UUID4

class Scenario(ScenarioBase):
    id: UUID4
    method_id: UUID4

    class Config:
        from_attributes = True