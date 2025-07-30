from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.database import get_session
from app.models.scenario import Scenario as ScenarioModel
from app.schemas.scenario import Scenario, ScenarioCreate, ScenarioResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.services.guideline_generator import GuidelineGenerator

router = APIRouter()

@router.post("/", response_model=ScenarioResponse)
async def create_scenario(
    scenario: ScenarioCreate,
    session: AsyncSession = Depends(get_session),
):
    try:
        # Format context with additional info for better guideline generation
        context_with_info = scenario.context
        if scenario.additional_info:
            context_with_info += "\n\nAdditional Info:\n"
            for key, value in scenario.additional_info.items():
                context_with_info += f"- {key}: {value}\n"
        
        # Generate guideline using the enhanced context
        guideline_result = await GuidelineGenerator.generate(context_with_info)
        
        new_scenario = ScenarioModel(
            id=uuid.uuid4(),
            title=guideline_result.title, 
            guideline=guideline_result.guideline,
            knowledge_foundation=guideline_result.knowledge_foundation,
            user_id=scenario.user_id,
        )
        session.add(new_scenario)
        await session.commit()
        await session.refresh(new_scenario)
        
        return new_scenario
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create scenario: {str(e)}")


@router.get("/{user_id}", response_model=List[ScenarioResponse])
async def read_scenarios(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    try:
        stmt = select(ScenarioModel).where(ScenarioModel.user_id == user_id).order_by(ScenarioModel.created_at.desc())
        result = await session.execute(stmt)
        scenarios = result.scalars().all()
        return scenarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scenarios: {str(e)}")


@router.get("/detail/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario_detail(
    scenario_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    try:
        stmt = select(ScenarioModel).where(ScenarioModel.id == scenario_id)
        result = await session.execute(stmt)
        scenario = result.scalar_one_or_none()
        
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
            
        return scenario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scenario: {str(e)}")


@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    try:
        stmt = select(ScenarioModel).where(ScenarioModel.id == scenario_id)
        result = await session.execute(stmt)
        scenario = result.scalar_one_or_none()
        
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        await session.delete(scenario)
        await session.commit()
        
        return {"message": "Scenario deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete scenario: {str(e)}")