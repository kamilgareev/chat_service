from typing import Any, Coroutine, Sequence

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Message, ChatType, Chat, User, Group, group_members


class ChatRepository:

    @staticmethod
    async def get_chat_history(
        session: AsyncSession,
        chat_id: int
    ) -> Sequence[Message]:
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create_personal_chat(
        session: AsyncSession,
        chat_name: str,
    ) -> Chat:
        chat = Chat(
            name=chat_name,
            type=ChatType.PERSONAL,
            group_id=None
        )
        session.add(chat)
        await session.commit()
        return chat

    @staticmethod
    async def create_group_chat(
        session: AsyncSession,
        chat_name: str,
        group_id: int,
    ) -> Chat:
        chat = Chat(
            name=chat_name,
            type=ChatType.GROUP,
            group_id=group_id
        )
        session.add(chat)
        await session.commit()
        return chat


class MessageRepository:

    @staticmethod
    async def create_message(
        session: AsyncSession,
        chat_id: int,
        sender_id: int,
        text: str
    ) -> Message:
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text
        )
        session.add(message)
        await session.commit()
        return message

    @staticmethod
    async def mark_message_as_read(
        session: AsyncSession,
        message_id: int
    ) -> None:
        await session.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(is_read=True)
        )
