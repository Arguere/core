from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.learning_path import LearningPath
from app.schemas.learning_path import LearningPath, LearningPathCreate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=LearningPath)
def create_learning_path(
    learning_path: LearningPathCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_learning_path = LearningPath(**learning_path.dict(), user_id=current_user.id)
    db.add(db_learning_path)
    db.commit()
    db.refresh(db_learning_path)
    return db_learning_path

@router.get("/", response_model=List[LearningPath])
def read_learning_paths(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(LearningPath).filter(LearningPath.user_id == current_user.id).all()