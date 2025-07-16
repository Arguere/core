from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.method import Method
from app.schemas.method import Method, MethodCreate
from app.dependencies.auth import get_current_user
from app.models.profile import Profile

router = APIRouter()

@router.post("/", response_model=Method)
def create_method(
    method: MethodCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    db_method = Method(**method.dict())
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method

@router.get("/{track_id}", response_model=List[Method])
def read_methods(
    track_id: int,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    return db.query(Method).filter(Method.track_id == track_id).all()