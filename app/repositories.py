from typing import Any, Coroutine, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Message, ChatType


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
    async def create_chat(
        session: AsyncSession,
        chat_name: str,
        chat_type: ChatType
    ):
        pass


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
        await session.refresh(message)
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
