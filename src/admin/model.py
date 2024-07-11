from pydantic import BaseModel

class Admin(BaseModel):
    login: str
    password: str
    email_code: str