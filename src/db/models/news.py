from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class NewsBase(SQLModel):
    title: str
    content: str
    category: Optional[str] = None


class News(NewsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=None)
    updated_at: Optional[datetime] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    title: Optional[str] = None  # type: ignore
    content: Optional[str] = None  # type: ignore
    category: Optional[str] = None


class NewsRead(NewsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
