from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import DBSessionDep
from app.models.scenario import Scenario
from app.schemas.scenario import Scenario, ScenarioCreate
from app.dependencies.auth import get_current_user
from app.models.profile import Profile
import uuid

router = APIRouter()

@router.post("/", response_model=Scenario)
async def create_scenario(
    scenario: ScenarioCreate,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    db_scenario = Scenario(id=uuid.uuid4(), **scenario.model_dump())
    db.add(db_scenario)
    await db.commit()
    await db.refresh(db_scenario)
    return db_scenario

@router.get("/{method_id}", response_model=List[Scenario])
async def read_scenarios(
    method_id: int,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    return await db.scalars(Scenario).filter(Scenario.method_id == method_id).all()