from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_session
from app.models.feedback import Feedback
from app.schemas.feedback import Feedback
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/{submission_id}", response_model=Feedback)
async def read_feedback(
    submission_id: int,
    session: AsyncSession = Depends(get_session),
):
    feedback = await session.execute(
        Feedback.select().where(Feedback.submission_id == submission_id)
    )
    feedback = feedback.scalars().first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return feedback