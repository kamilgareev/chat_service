from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, String, Enum as EnumColumn, ForeignKey, Table, func, Index, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    messages: Mapped[list['Message']] = relationship(
        back_populates='sender'
    )
    groups: Mapped[list['Group']] = relationship(
        secondary='group_members',
        back_populates='members'
    )
    created_groups: Mapped[list['Group']] = relationship(
        back_populates='creator'
    )


class ChatType(str, Enum):
    PRIVATE = 'private'
    GROUP = 'group'


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[ChatType] = mapped_column(EnumColumn(ChatType), default=ChatType.PRIVATE)

    messages: Mapped[list['Message']] = relationship(
        back_populates='chat',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    creator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )

    creator: Mapped[Optional[User]] = relationship(back_populates='created_groups')
    members: Mapped[list[User]] = relationship(
        secondary='group_members',
        back_populates='groups'
    )


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = (
        Index('idx_messages_chat_id_timestamp', 'chat_id', 'timestamp')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        default=uuid4
    )
    text: Mapped[str] = mapped_column(String(4096), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    is_read: Mapped[bool] = mapped_column(default=False)

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    sender_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )

    chat: Mapped[Chat] = relationship(back_populates='messages')
    sender: Mapped[Optional[User]] = relationship(back_populates='messages')


group_members = Table(
    'group_members',
    Base.metadata,
    Column('group_id', ForeignKey('groups.id'), primary_key=True, index=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True, index=True)
)
