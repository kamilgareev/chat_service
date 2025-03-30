from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Message


class ChatRepository:

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
    async def get_chat_history(
            session: AsyncSession,
            chat_id: int
    ):
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
        )
        result = await session.execute(query)
        return result.scalars().all()
