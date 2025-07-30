from pydantic import BaseModel, Field, UUID4
from datetime import datetime

class SubmissionCreate(BaseModel):
    scenario_id: UUID4


class Submission(BaseModel):
    id: UUID4
    scenario_id: UUID4
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config: 
        from_attributes = True

