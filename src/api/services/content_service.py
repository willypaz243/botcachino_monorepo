from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.db.models.content import Content, ContentCreate, ContentUpdate


class ContentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_content(self, content_in: ContentCreate) -> Content:
        new_content = Content(**content_in.model_dump())
        # Placeholder for embedding generation logic
        new_content.embedding = [0.0] * 4096
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
