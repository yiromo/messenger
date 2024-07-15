from typing import List
from tortoise.transactions import in_transaction
from .model import Chat, ChatUser, ChatLine
from user.service import user_service
from tortoise import Tortoise
from config import settings
from postgre import pg

async def init():
    await Tortoise.init(
        db_url=settings.POSTGRES_URL,
        modules={'models': ['chat.model']},
    )
    await Tortoise.generate_schemas()

class ChatService:
    async def create_chat(self) -> Chat:
        table_name = 'chat'
        await pg.create_table_if_not_exists(table_name, [
            'id SERIAL PRIMARY KEY'
        ])
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
        return user

    async def update_message(self, chat_id: str, message_id: int, message: str) -> ChatLine:
        chat_line = await ChatLine.filter(chat_id=chat_id, id=message_id).first()
        if chat_line:
            chat_line.line_text = message
            await chat_line.save()
            return chat_line
        return None

    async def send_message(self, chat_id: int, user_id: int, message: str) -> ChatLine:
        chat = await Chat.get(id=chat_id)
        user = await ChatUser.get(id=user_id)
        if chat and user:
            chat_line = await ChatLine.create(chat_id=chat_id, user_id=user_id, line_text=message)
            return chat_line
        return None

    async def get_chat_lines(self, chat_id: str) -> List[ChatLine]:
        return await ChatLine.filter(chat_id=chat_id).order_by('created_at').all()

chat_service = ChatService()