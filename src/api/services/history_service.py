from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.db.models.history import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    Message,
    MessageCreate,
)


class HistoryService:
    def __init__(self, session: AsyncSession):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    async def create_conversation(self, conversation_in: ConversationCreate) -> Conversation:
        new_conversation = Conversation(**conversation_in.model_dump())
        self.session.add(new_conversation)
        await self.session.commit()
        await self.session.refresh(new_conversation)
        return new_conversation

    async def get_all_conversations(self, limit: int = 50, offset: int = 0) -> list[Conversation]:
        query = select(Conversation).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_conversation_by_uuid(self, uuid: str) -> Conversation | None:
        return await self.session.get(Conversation, uuid)

    async def update_conversation(
        self, uuid: str, conversation_in: ConversationUpdate
    ) -> Conversation | None:
        conversation = await self.session.get(Conversation, uuid)
        if not conversation:
            return None

        data = conversation_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(conversation, key, value)

        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def delete_conversation(self, uuid: str) -> bool:
        conversation = await self.session.get(Conversation, uuid)
        if not conversation:
            return False
        await self.session.delete(conversation)
        await self.session.commit()
        return True

    async def add_message(
        self, conversation_uuid: str, message_in: MessageCreate
    ) -> Message | None:
        conversation = await self.session.get(Conversation, conversation_uuid)
        if not conversation:
            return None

        new_message = Message(
            **message_in.model_dump(),
            conversation_uuid=UUID(conversation_uuid),
        )
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return new_message

    async def get_messages(
        self, conversation_uuid: str, limit: int = 100, offset: int = 0
    ) -> list[Message]:
        query = (
            select(Message)
            .where(col(Message.conversation_uuid) == UUID(conversation_uuid))  # type: ignore[arg-type]
            .order_by(col(Message.timestamp))  # type: ignore[arg-type]
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_message_by_id(self, message_id: str) -> Message | None:
        return await self.session.get(Message, message_id)

    async def delete_message(self, message_id: str) -> bool:
        message = await self.session.get(Message, message_id)
        if not message:
            return False
        await self.session.delete(message)
        await self.session.commit()
        return True

    async def clear_conversation_messages(self, conversation_uuid: str) -> bool:
        conversation = await self.session.get(Conversation, conversation_uuid)
        if not conversation:
            return False

        query = select(Message).where(col(Message.conversation_uuid) == UUID(conversation_uuid))  # type: ignore[arg-type]
        result = await self.session.execute(query)
        messages = result.scalars().all()

        for message in messages:
            await self.session.delete(message)

        await self.session.commit()
        return True
