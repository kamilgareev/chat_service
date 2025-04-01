from typing import Sequence

from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import Container
from app.db.models import Message, Chat, Group
from app.core.repositories import ChatRepository, MessageRepository, GroupRepository, UserRepository
from core.exceptions.not_found_exceptions import ChatNotFoundException, MessageNotFoundException


class ChatService:

    @inject
    def __init__(
        self,
        chat_repository: ChatRepository = Provide[Container.chat_repository],
        message_repository: MessageRepository = Provide[Container.message_repository]
    ):
        self.chat_repo = chat_repository
        self.msg_repo = message_repository

    async def get_chat_history(
        self,
        session: AsyncSession,
        chat_id: int
    ) -> Sequence[Message]:
        if not self.chat_repo.chat_exists(
            session, chat_id
        ):
            raise ChatNotFoundException()
        return await self.chat_repo.get_chat_history(
            session, chat_id
        )

    async def create_personal_chat(
        self,
        session: AsyncSession,
        chat_name: str
    ) -> Chat:
        return await self.chat_repo.create_personal_chat(
            session, chat_name
        )

    async def create_group_chat(
        self,
        session: AsyncSession,
        chat_name: str,
        group_id: int
    ) -> Chat:
        return await self.chat_repo.create_group_chat(
            session, chat_name, group_id
        )

    async def send_message(
        self,
        session: AsyncSession,
        chat_id: int,
        sender_id: int,
        text: str,
    ) -> Message:
        if not self.chat_repo.chat_exists(
            session, chat_id
        ):
            raise ChatNotFoundException()
        return await self.msg_repo.create_message(
            session, chat_id, sender_id, text
        )

    async def mark_message_as_read(
        self,
        session: AsyncSession,
        message_id: int
    ) -> None:
        if not self.msg_repo.message_exists(
            session, message_id
        ):
            raise MessageNotFoundException()
        await self.msg_repo.mark_message_as_read(
            session, message_id
        )


class GroupService:

    @inject
    def __init__(
        self,
        group_repository: GroupRepository = Provide[Container.group_repository]
    ):
        self.repo = group_repository

    async def create_group(
        self,
        session: AsyncSession,
        group_name: str,
        creator_id: int,
        members_ids: list[int]
    ) -> Group:
        return await self.repo.create_group(
            session, group_name, creator_id, members_ids
        )


class UserService:
    """
    Понадобится в будущем, для MVP оставим так.
    """

    @inject
    def __init__(
        self,
        user_repository: UserRepository = Provide[Container.user_repository]
    ):
        self.repo = user_repository


class Service:

    @inject
    def __init__(
        self,
        chat_service: ChatService = Provide[Container.chat_service],
        group_service: GroupService = Provide[Container.group_service],
        user_service: UserService = Provide[Container.user_service]
    ):
        self.chats = chat_service
        self.groups = group_service
        self.users = user_service
