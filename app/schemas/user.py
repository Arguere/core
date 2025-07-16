from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, Dict, List

class User(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    onboarding_options: Optional[Dict[str, List[str]]] = None
    created_at: datetime

    class Config:
        orm_mode = True
