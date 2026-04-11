from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.info import Info, InfoCreate, InfoUpdate


class InfoService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_info(self, skip: int = 0, limit: int = 100) -> List[Info]:
        statement = select(Info).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_info(self, info_id: int) -> Optional[Info]:
        return await self.session.get(Info, info_id)

    async def create_info(self, info: InfoCreate) -> Info:
        from datetime import datetime

        db_info = Info.model_validate(info)
        db_info.created_at = datetime.utcnow()
        self.session.add(db_info)
        await self.session.commit()
        await self.session.refresh(db_info)
        return db_info

    async def update_info(
        self, info_id: int, info_update: InfoUpdate
    ) -> Optional[Info]:
        db_info = await self.session.get(Info, info_id)
        if not db_info:
            return None

        update_data = info_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_info, key, value)

        self.session.add(db_info)
        await self.session.commit()
        await self.session.refresh(db_info)
        return db_info

    async def delete_info(self, info_id: int) -> bool:
        db_info = await self.session.get(Info, info_id)
        if not db_info:
            return False

        await self.session.delete(db_info)
        await self.session.commit()
        return True
