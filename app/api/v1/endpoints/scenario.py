from fastapi import APIRouter, Depends
from typing import List
from app.core.database import get_session
from app.models.scenario import Scenario as ScenarioModel
from app.schemas.scenario import Scenario, ScenarioCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid


from app.services.guideline_generator import GuidelineGenerator

router = APIRouter()

# TODO: call guideline creation service
@router.post("/", response_model=Scenario)
async def create_scenario(
    scenario: ScenarioCreate,
    session: AsyncSession = Depends(get_session),
):
    guideline_result = await GuidelineGenerator.generate(scenario.context)
    
    new_scenario = ScenarioModel(
        id=uuid.uuid4(), # TODO: make the database generate the uuid
        title = guideline_result.title, 
        guideline=guideline_result.guideline,
        knowledge_foundation=guideline_result.knowledge_foundation,
        user_id=scenario.user_id,
    )
    session.add(new_scenario)
    await session.commit()
    await session.refresh(new_scenario)
    
    return new_scenario


@router.get("/{user_id}", response_model=List[Scenario])
async def read_scenarios(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    stmt = select(ScenarioModel).where(ScenarioModel.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
