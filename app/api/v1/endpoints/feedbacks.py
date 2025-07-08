from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import Feedback
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/{submission_id}", response_model=Feedback)
def read_feedback(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    feedback = db.query(Feedback).filter(Feedback.submission_id == submission_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback