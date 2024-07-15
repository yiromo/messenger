from .model import AdminOutLogin
from pymongo.collection import Collection
from fastapi import HTTPException, status, Response
from mongodb import db
from passlib.context import CryptContext
import uuid
from utils.token import create_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService:
    def __init__(self, collection: str):
        self.collection: Collection = db.db[collection]

    async def authenticate_user(
        self, username: str, password: str, response: Response
    ) -> AdminOutLogin:
        user = await self.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if not password_context.verify(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token = await create_token(
            data={
                "sub": user["id"],
                "role": user["role"],
            },
            token_type="access",
        )
        refresh_token = await create_token(
            data={
                "sub": user["id"],
                "role": user["role"],
            },
            token_type="refresh",
        )

        return AdminOutLogin(accessToken=access_token, refreshToken=refresh_token)

    async def get_user_by_username(self, username: str) -> dict:
        user = await self.collection.find_one({"username": username})
        return user


admin_service = AdminService("admins")