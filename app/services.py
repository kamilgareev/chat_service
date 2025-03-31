from typing import Sequence

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.db.models import Message, Chat
from app.repositories import ChatRepository, MessageRepository


class ChatService:

    @inject
    def __init__(
        self,
        chat_repository: ChatRepository = Provide[Container.chat_repository]
    ):
        self.repo = chat_repository

    async def get_chat_history(
        self,
        session: AsyncSession,
        chat_id: int
    ) -> Sequence[Message]:
        return await self.repo.get_chat_history(
            session, chat_id
        )

    async def create_personal_chat(
        self,
        session: AsyncSession,
        chat_name: str
    ) -> Chat:
        return await self.repo.create_personal_chat(
            session, chat_name
        )

    async def create_group_chat(
        self,
        session: AsyncSession,
        chat_name: str,
        group_id: int
    ) -> Chat:
        return await self.repo.create_group_chat(
            session, chat_name, group_id
        )


class MessageService:

    @inject
    def __init__(
        self,
        message_repository: MessageRepository = Provide[Container.message_repository]
    ):
        self.repo = message_repository

    async def send_message(
        self,
        session: AsyncSession,
        chat_id: int,
        sender_id: int,
        text: str,
    ) -> Message:
        return await self.repo.create_message(
            session, chat_id, sender_id, text
        )

    async def mark_message_as_read(
        self,
        session: AsyncSession,
        message_id: int
    ) -> None:
        await self.repo.mark_message_as_read(
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
