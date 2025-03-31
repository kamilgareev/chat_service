from typing import Sequence

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.db.models import Message
from app.repositories import ChatRepository, MessageRepository


class ChatService:

    @inject
    def __init__(
        self,
        chat_repo: ChatRepository = Provide[Container.chat_repository]
    ):
        self.chat_repo = chat_repo

    async def get_chat_history(
        self,
        session: AsyncSession,
        chat_id: int
    ) -> Sequence[Message]:
        return await self.chat_repo.get_chat_history(
            session, chat_id
        )


class MessageService:

    @inject
    def __init__(
        self,
        message_repo: MessageRepository = Provide[Container.message_repository]
    ):
        self.message_repo = message_repo

    async def send_message(
        self,
        session: AsyncSession,
        chat_id: int,
        sender_id: int,
        text: str,
    ) -> Message:
        return await self.message_repo.create_message(
            session, chat_id, sender_id, text
        )

    async def mark_message_as_read(
        self,
        session: AsyncSession,
        message_id: int
    ) -> None:
        await self.message_repo.mark_message_as_read(
            session, message_id
        )


class Service:

    @inject
    def __init__(
        self,
        chat_service: ChatService = Provide[Container.chat_service],
        message_service: MessageService = Provide[Container.message_service]
    ):
        self.chats = chat_service
        self.messages = message_service
