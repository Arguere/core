from pydantic import BaseModel
from typing import Optional

class ScenarioBase(BaseModel):
    title: str
    description: Optional[str] = None

class ScenarioCreate(ScenarioBase):
    method_id: int

class Scenario(ScenarioBase):
    id: int
    method_id: int

    class Config:
        orm_mode = True