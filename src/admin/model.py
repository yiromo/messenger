from pydantic import BaseModel, Field
from base.models import AsyncBaseModel, IdBase

class Admin(AsyncBaseModel):
    login: str
    password: str

class AdminOutLogin(BaseModel):
    accessToken: str = Field(alias="accessToken", title="Access Token")
    refreshToken: str = Field(alias="refreshToken", title="Refresh Token")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AdminAccessToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True