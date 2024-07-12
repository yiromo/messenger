from fastapi import HTTPException, APIRouter, Depends, Response, Form
from .service import admin_service
from .model import AdminAccessToken
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/login/", response_model=AdminAccessToken, status_code=201)
async def sign_in(response: Response, username: str = Form(...), password: str = Form(...)):
    access_token = await admin_service.authenticate_user(username=username, password=password, response=response)
    return {"access_token": access_token.accessToken, "token_type": "Bearer"}
