from base.models import PyObjectId
from pydantic import BaseModel, Field
from typing import Optional

class Login(BaseModel):
    id: PyObjectId = Field(default=PyObjectId, alias="_id")    
    username: str
    password: str

class Register(Login):
    repass: str

class Token(BaseModel):
    access_token: str
    token_type: str