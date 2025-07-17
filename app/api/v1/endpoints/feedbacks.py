from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import DBSessionDep
from app.models.feedback import Feedback
from app.schemas.feedback import Feedback
from app.dependencies.auth import get_current_user
from app.models.profile import Profile

router = APIRouter()

@router.get("/{submission_id}", response_model=Feedback)
async def read_feedback(
    submission_id: int,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    feedback = await db.query(Feedback).filter(Feedback.submission_id == submission_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback