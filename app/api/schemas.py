from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    uuid: uuid4
    text: str
    timestamp: datetime
    is_read: bool
    chat_id: int
    sender_id: int


class ChatSchema(BaseModel):
    id: int
    name: str
    type: str
    group_id: int | None


class ChatCreateSchema(BaseModel):
    name: str

class PersonalChatCreateSchema(ChatCreateSchema):
   pass

class GroupChatCreateSchema(ChatCreateSchema):
    group_id: int