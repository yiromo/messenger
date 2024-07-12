from pydantic import BaseModel
from typing import Optional, List
from base.models import IdBase

class UserRead(BaseModel):
    objectId: str
    id: str
    username: str
    role: str
    email: Optional[str] = None
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True