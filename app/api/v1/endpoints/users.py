from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user["sub"],
        "email": current_user.get("email"),
        "claims": current_user
    }
