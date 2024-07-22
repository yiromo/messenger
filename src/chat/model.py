from tortoise.models import Model
from pydantic import BaseModel
from tortoise import fields
import uuid

class Chat(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)

class ChatUser(Model):
    id = fields.BigIntField(pk=True, generated=True)
    obj_id = fields.CharField(max_length=255, unique=True) 


class ChatLine(Model):
    id = fields.BigIntField(pk=True, generated=True)
    chat = fields.ForeignKeyField('models.Chat', related_name='lines', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.ChatUser', related_name='lines', on_delete=fields.CASCADE)
    line_text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        indexes = [
            ("chat_id",),
            ("user_id",)
        ]

class ChatLineResponse(BaseModel):
    id: int
    chat_id: uuid.UUID
    user_id: int
    line_text: str
    created_at: str

