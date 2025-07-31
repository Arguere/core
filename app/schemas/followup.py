from pydantic import BaseModel, Json
from typing import Dict

class GeneratedFollowUp(BaseModel):
    status: str  # "follow-up-needed" or "sufficient"
    follow_up_questions: Json  # List of follow-up questions in JSON format

    class Config:
        json_encoders = {
            Json: lambda v: v if isinstance(v, str) else str(v)
        }