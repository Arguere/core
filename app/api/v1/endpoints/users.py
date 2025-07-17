from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "onboarding_options": current_user.onboarding_options,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
    }
