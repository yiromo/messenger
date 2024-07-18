from typing import List
from tortoise.transactions import in_transaction
from .model import Chat, ChatUser, ChatLine
from user.service import user_service
from tortoise import Tortoise
from config import settings
from postgre import pg
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from crypto.utils import CryptoUtils
import base64

async def init():
    await Tortoise.init(
        db_url=settings.POSTGRES_URL,
        modules={'models': ['chat.model']},
    )
    await Tortoise.generate_schemas()

class ChatService:    
    async def create_chat(self) -> Chat:
        table_name = 'chat'
        await pg.create_table_if_not_exists(table_name, ['id SERIAL PRIMARY KEY'])
        return await Chat.create()
    
    async def add_user(self, obj_id: str) -> ChatUser:
        existing_user = await ChatUser.filter(obj_id=obj_id).first()
        if existing_user:
            return existing_user
        user = await ChatUser.create(obj_id=obj_id)
        return user

    async def add_user_to_chat(self, chat_id, user_id: int) -> ChatUser:
        chat = await Chat.get(id=chat_id)
        user = await ChatUser.get(id=user_id)
        if chat and user:
            return user
        return None

    async def update_message(self, chat_id: str, message_id: int, message: str, recipient_private_key: RSAPrivateKey) -> ChatLine:
        chat_line = await ChatLine.filter(chat_id=chat_id, id=message_id).first()
        if chat_line:
            decrypted_message = CryptoUtils.decrypt_message(base64.b64decode(chat_line.line_text), recipient_private_key)
            chat_line.line_text = decrypted_message
            await chat_line.save()
            return chat_line
        return None

    async def send_message(self, chat_id: int, user_id: int, message: str, recipient_public_key: RSAPublicKey) -> ChatLine:
        encrypted_message = CryptoUtils.encrypt_message(message, recipient_public_key)
        encrypted_message_base64 = base64.b64encode(encrypted_message).decode('utf-8')
        chat = await Chat.get(id=chat_id)
        user = await ChatUser.get(id=user_id)
        if chat and user:
            chat_line = await ChatLine.create(chat_id=chat_id, user_id=user_id, line_text=encrypted_message_base64)
            return chat_line
        return None

    async def get_chat_lines(self, chat_id: str, recipient_private_key) -> List[dict]:
        chat_lines = await ChatLine.filter(chat_id=chat_id).order_by('created_at').all()
        decrypted_chat_lines = []
        for line in chat_lines:
            decrypted_message = CryptoUtils.decrypt_message(base64.b64decode(line.line_text), recipient_private_key)
            decrypted_chat_lines.append({**line.dict(), 'line_text': decrypted_message})
        return decrypted_chat_lines

chat_service = ChatService()