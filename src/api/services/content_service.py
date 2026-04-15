from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.db.models.content import Content, ContentCreate, ContentUpdate

from .embedding_service import EmbbedingService


class ContentService:
    def __init__(self, session: AsyncSession, emb_service: EmbbedingService):
        self.__session = session
        self.__emb_service = emb_service

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @property
    def emb_service(self) -> EmbbedingService:
        return self.__emb_service

    async def create_content(self, content_in: ContentCreate) -> Content:
        text_content = (
            f"#{self.emb_service.pre_process_text(content_in.title)}\n\n"
            f"## Summary\n{self.emb_service.pre_process_text(content_in.summary)}\n\n"
            f"## Content\n{self.emb_service.pre_process_text(content_in.content)}"
        )

        new_content = Content(**content_in.model_dump())
        new_content.embedding = self.emb_service.embed_text(text_content)

        self.session.add(new_content)
        await self.session.commit()
        await self.session.refresh(new_content)
        return new_content

    async def get_all_contents(self) -> list[Content]:
        result = await self.session.execute(select(Content))
        return list(result.scalars().all())

    async def get_content_by_id(self, content_int: int) -> Content | None:
        return await self.session.get(Content, content_int)

    async def update_content(self, content_id: int, content_in: ContentUpdate) -> Content | None:
        content = await self.session.get(Content, content_id)
        if not content:
            return None

        data = content_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(content, key, value)

        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def delete_content(self, content_id: int) -> bool:
        content = await self.session.get(Content, content_id)
        if not content:
            return False
        await self.session.delete(content)
        await self.session.commit()
        return True

    async def search(self, query_text: str, limit: int = 5, offset: int = 0) -> list[Content]:
        normalized_text = self.emb_service.pre_process_text(query_text)
        query_embedding = self.emb_service.embed_text(normalized_text)

        query = (
            select(Content)
            .order_by(col(Content.embedding).op("<=>")(query_embedding))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        contents = list(result.scalars().all())

        return contents

    async def get_by_ids(self, ids: list[int]) -> list[Content]:
        if not ids:
            return []

        query = select(Content).where(Content.id.in_(ids))
        result = await self.session.execute(query)
        contents = list(result.scalars().all())

        return contents

    def format_content_for_agent(self, content: Content) -> dict:
        return {
            "id": content.id,
            "title": content.title,
            "category": content.category.value,
            "content": content.content,
            "post_date": content.post_date.isoformat() if content.post_date else None,
        }

    def format_content_summary(self, content: Content) -> dict:
        return {
            "id": content.id,
            "summary": content.summary,
        }
