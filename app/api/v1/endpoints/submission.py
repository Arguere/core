from fastapi import APIRouter, Depends
from typing import List
from app.core.database import get_session
from app.models.submission import Submission
from app.schemas.scenario import ScenarioCreate
from app.schemas.submission import Submission 
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/", response_model=Submission)
async def create_submission(
    scenario: ScenarioCreate,
    session: AsyncSession = Depends(get_session)): 
    
    pass

@router.get("/{scenario_id}", response_model=List[Submission])
async def read_submissions(
    scenario_id: int,
    session: AsyncSession = Depends(get_session),
):
    submissions = await session.execute(
        Submission.select().where(Submission.scenario_id == scenario_id)
    )
    return submissions.scalars().all()