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

    async def add_user_to_chat(self, chat_id: int, user_id: int) -> ChatUser:
        chat = await Chat.get(id=chat_id)
        user = await user_service.get_user_by_objid(user_id) 
        if chat and user:
            chat_user = await ChatUser.create(chat_id=chat_id, user_id=user_id)
            return chat_user
        return None

    async def send_message(self, chat_id: int, user_id: int, message: str) -> ChatLine:
        chat = await Chat.get(id=chat_id)
        user = await user_service.get_user_by_objid(user_id)
        if chat and user:
            chat_line = await ChatLine.create(chat_id=chat_id, user_id=user_id, line_text=message)
            return chat_line
        return None

    async def get_chat_lines(self, chat_id: int) -> List[ChatLine]:
        return await ChatLine.filter(chat_id=chat_id).order_by('created_at').all()

chat_service = ChatService()