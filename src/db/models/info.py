from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class InfoBase(SQLModel):
    title: str
    content: str
    category: Optional[str] = None


class Info(InfoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=None)
    updated_at: Optional[datetime] = None


class InfoCreate(InfoBase):
    pass


class InfoUpdate(InfoBase):
    title: Optional[str] = None  # type: ignore
    content: Optional[str] = None  # type: ignore
    category: Optional[str] = None


class InfoRead(InfoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
