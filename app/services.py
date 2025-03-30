from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from containers import Container
from repositories import ChatRepository


class ChatService:

    @inject
    def __init__(
            self,
            chat_repository: ChatRepository = Provide[Container.chat_repository]
    ):
        self.chat_repository = chat_repository







