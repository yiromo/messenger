from pydantic import BaseModel
from typing import Optional, List
from base.models import IdBase

class UserBase(BaseModel):
    objectId: str
    id: str
    username: str
    role: str
    email: Optional[str] = None
    profile_picture: Optional[str] = None
    is_private: Optional[bool] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: str
    username: str
    profile_picture: Optional[str] = None
    is_private: Optional[bool] = None
    is_active: Optional[bool] = True
