from .model import UserOutLogin
from pymongo.collection import Collection
from fastapi import HTTPException, status, Response
from mongodb import db
from passlib.context import CryptContext
import uuid
from utils.token import create_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, collection: str):
        self.collection: Collection = db.db[collection]

    async def authenticate_user(
        self, username: str, password: str, response: Response
    ) -> UserOutLogin:
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

        return UserOutLogin(accessToken=access_token, refreshToken=refresh_token)

    async def create_user(self, username, password):
        user = await self.collection.find_one({"username": username})
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = password_context.hash(password)
        user_id = str(uuid.uuid4())
        await self.collection.insert_one(
            {"id": user_id, "username": username, "password": hashed_password, "role": username}
        )
        access_token = await create_token(data={"sub": user_id, "role": username})
        refresh_token = await create_token(
            data={"sub": user_id, "role": username}, token_type="refresh"
        )
        return UserOutLogin(accessToken=access_token, refreshToken=refresh_token)

    async def get_user_by_username(self, username: str) -> dict:
        user = await self.collection.find_one({"username": username})
        return user


auth_service = UserService("users")