from fastapi import HTTPException, APIRouter, Response, Form
from .model import UserLoginBase, UserAccessToken, UserOutLogin
from .service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/sign-up/", response_model=UserOutLogin)
async def sign_up(user: UserLoginBase):
    token_obj = await auth_service.create_user(
        username=user.username, password=user.password
    )
    return {
        "accessToken": token_obj.accessToken,
        "refreshToken": token_obj.refreshToken,
        "token_type": "Bearer",}

@router.post("/login/", response_model=UserAccessToken, status_code=201)
async def sign_in(response: Response, username: str = Form(...), password: str = Form(...)):
    access_token = await auth_service.authenticate_user(username=username, password=password, response=response)
    return {"access_token": access_token.accessToken, "token_type": "Bearer"}

