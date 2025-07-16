from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.track import Track
from app.schemas.track import Track, TrackCreate
from app.dependencies.auth import get_current_user
from app.models.profile import Profile

router = APIRouter()

@router.post("/", response_model=Track)
def create_track(
    track: TrackCreate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    db_track = Track(**track.model_dump(), user_id=current_user.id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

@router.get("/", response_model=List[Track])
def read_tracks(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    return db.query(Track).filter(Track.user_id == current_user.id).all()