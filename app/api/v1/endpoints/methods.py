from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import DBSessionDep
from app.models.method import Method
from app.schemas.method import Method, MethodCreate
from app.dependencies.auth import get_current_user
from app.models.profile import Profile

router = APIRouter()

@router.post("/", response_model=Method)
async def create_method(
    method: MethodCreate,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    db_method = Method(**method.model_dump())
    db.add(db_method)
    await db.commit()
    await db.refresh(db_method)
    return db_method

@router.get("/{track_id}", response_model=List[Method])
async def read_methods(
    track_id: int,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    return await db.query(Method).filter(Method.track_id == track_id).all()