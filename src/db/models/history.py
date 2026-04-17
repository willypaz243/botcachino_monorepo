from datetime import datetime
from typing import List
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel, Column, DateTime, text

class Role(str, Enum):
    USER = "user"
    BOT = "bot"

class MessageBase(SQLModel):
    role: Role
    content: str
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("now()"),
            nullable=False,
        ),
    )

class Message(MessageBase, table=True):
    __tablename__ = "messages"

    uuid: UUID = Field(
        default_factory=uuid4, 
        primary_key=True, 
        index=True, 
        nullable=False
    )
    conversation_uuid: UUID = Field(foreign_key="conversations.uuid", index=True)

    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    pass

class ConversationBase(SQLModel):
    title: str


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    uuid: UUID = Field(
        default_factory=uuid4, 
        primary_key=True, 
        index=True, 
        nullable=False
    )

    messages: List[Message] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
    )


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: str | None = None


class ConversationRead(ConversationBase):
    pass