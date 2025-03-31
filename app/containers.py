from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.settings import settings
from repositories import ChatRepository, MessageRepository
from services import ChatService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_engine = providers.Singleton(
        create_async_engine,
        settings.db.DB_URL
    )
    db_session = providers.Factory(
        async_sessionmaker,
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    chat_repository = providers.Factory(
        ChatRepository
    )
    message_repository = providers.Factory(
        MessageRepository
    )

    chat_service = providers.Factory(
        ChatService,
        chat_repository=chat_repository
    )
