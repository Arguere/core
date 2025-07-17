from fastapi import APIRouter, Depends, HTTPException

from typing import List
from app.core.database import DBSessionDep
from app.models.track import Track as TrackModel
from app.schemas.track import Track, TrackCreate
from app.dependencies.auth import get_current_user
from app.models.profile import Profile
from sqlalchemy.future import select
import uuid

router = APIRouter()

@router.post("/", response_model=Track)
async def create_track(
    track: TrackCreate,
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    db_track = TrackModel(id=uuid.uuid4(), **track.model_dump(), user_id=current_user.id)
    db.add(db_track)
    await db.commit()
    await db.refresh(db_track)
    return db_track

@router.get("/", response_model=List[Track])
async def read_tracks(
    db: DBSessionDep,
    current_user: Profile = Depends(get_current_user)
):
    result = await db.scalars(select(TrackModel).filter_by(user_id=current_user.id))
    return result.all()