from pydantic import BaseModel, Json
from typing import Dict

class GeneratedGuideline(BaseModel):
    title: str
    knowledge_foundation: str
    guideline: Dict[str, str]
