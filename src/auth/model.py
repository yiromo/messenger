from base.models import PyObjectId, IdBase, AsyncBaseModel
from pydantic import BaseModel, Field
from bson import ObjectId

class UserLoginBase(AsyncBaseModel): 
    #username_id: str = Field(alias="usernameId", title="Username ID", default=None)  
    username: str 
    password: str 

    #class Config:
    #    populate_by_name = True
    #    arbitrary_types_allowed = True
    #    json_encoders = {ObjectId: str}

class UserOutLogin(BaseModel):
    accessToken: str = Field(alias="accessToken", title="Access Token")
    refreshToken: str = Field(alias="refreshToken", title="Refresh Token")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
    
class UserAccessToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True