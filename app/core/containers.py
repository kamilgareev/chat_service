from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.settings import settings
from app.core.repositories import ChatRepository, MessageRepository, GroupRepository, UserRepository
from app.core.services import Service, ChatService, GroupService, UserService


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
    group_repository = providers.Factory(
        GroupRepository
    )
    user_repository = providers.Factory(
        UserRepository
    )

    # Services
    chat_service = providers.Factory(
        ChatService,
        chat_repository=chat_repository
    )
    group_service = providers.Factory(
        GroupService,
        group_repository=group_repository
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

    service = providers.Factory(
        Service,
        chat_service=chat_service,
        group_service=group_service,
        user_service=user_service
    )
