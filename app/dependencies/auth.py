from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
import supabase
from app.models.profile import Profile

security = HTTPBearer()
SUPABASE_JWT_SECRET = settings.SUPABASE_JWT_SECRET

def verify_supabase_jwt(token: str):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase credentials"
        ) from e

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Profile:
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return Profile(
            id=response.user.id,
            email=response.user.email,
            full_name=response.user.user_metadata.get("full_name", ""),
            onboarding_options=response.user.user_metadata.get("onboarding_options", []),
            created_at=response.user.created_at,
            updated_at=response.user.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth error: {str(e)}")
    
