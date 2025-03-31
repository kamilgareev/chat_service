from typing import Sequence

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from containers import Container
from db.models import Message
from repositories import ChatRepository, MessageRepository


class Service:

    @inject
    def __init__(
        self,
        chat_repository: ChatRepository = Provide[Container.chat_repository],
        message_repository: MessageRepository = Provide[Container.message_repository]
    ):
        self.chat_repository = chat_repository
        self.message_repository = message_repository

    async def send_message(
        self,
        session: AsyncSession,
        chat_id: int,
        sender_id: int,
        text: str,
    ) -> Message:
        return await self.chat_repository.create_message(
            session, chat_id, sender_id, text
        )

    async def mark_message_as_read(
        self,
        session: AsyncSession,
        message_id: int
    ) -> None:
        await self.chat_repository.mark_message_as_read(
            session, message_id
        )

    async def get_chat_history(
        self,
        session: AsyncSession,
        chat_id: int
    ) -> Sequence[Message]:
        return await self.chat_repository.get_chat_history(
            session, chat_id
        )
