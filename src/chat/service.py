from .model import UserOutLogin
from pymongo.collection import Collection
from fastapi import HTTPException, status, Response
from db import db
from passlib.context import CryptContext
import uuid
from utils.token import create_token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, collection: str):
        self.collection: Collection = db.db[collection]


user_service = UserService("chats")