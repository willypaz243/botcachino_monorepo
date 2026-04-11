from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.news import News, NewsCreate, NewsUpdate


class NewsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_news(self, skip: int = 0, limit: int = 100) -> List[News]:
        statement = select(News).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_news(self, news_id: int) -> Optional[News]:
        return await self.session.get(News, news_id)

    async def create_news(self, news: NewsCreate) -> News:
        from datetime import datetime

        db_news = News.model_validate(news)
        db_news.created_at = datetime.utcnow()
        self.session.add(db_news)
        await self.session.commit()
        await self.session.refresh(db_news)
        return db_news

    async def update_news(
        self, news_id: int, news_update: NewsUpdate
    ) -> Optional[News]:
        db_news = await self.session.get(News, news_id)
        if not db_news:
            return None

        update_data = news_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_news, key, value)

        self.session.add(db_news)
        await self.session.commit()
        await self.session.refresh(db_news)
        return db_news

    async def delete_news(self, news_id: int) -> bool:
        db_news = await self.session.get(News, news_id)
        if not db_news:
            return False

        await self.session.delete(db_news)
        await self.session.commit()
        return True
