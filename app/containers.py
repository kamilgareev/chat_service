from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.settings import settings
from app.repositories import ChatRepository, MessageRepository
from app.services import Service, ChatService, MessageService


class Container(containers.DeclarativeContainer):
    # DB
    db_engine = providers.Singleton(
        create_async_engine,
        settings.db.db_url
    )
    db_session = providers.Factory(
        async_sessionmaker,
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Repos
    chat_repository = providers.Factory(
        ChatRepository
    )
    message_repository = providers.Factory(
        MessageRepository
    )

    # Services
    chat_service = providers.Factory(
        ChatService,
        chat_repository=chat_repository
    )
    message_service = providers.Factory(
        MessageService,
        message_repository=message_repository
    )
    service = providers.Factory(
        Service,
        chat_service=chat_service,
        message_service=message_service
    )
