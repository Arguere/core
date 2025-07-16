from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user["sub"],
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name"),
        "onboarding_options": current_user.get("onboarding_options"),
        "created_at": current_user.get("created_at"),
        "updated_at": current_user.get("updated_at"),
    }
