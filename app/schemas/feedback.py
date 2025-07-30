from pydantic import BaseModel, UUID4
from datetime import datetime

class FeedbackBase(BaseModel):
    submission_id: UUID4
    content: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True

