from datetime import datetime
from enum import Enum

from pgvector.sqlalchemy import VECTOR
from sqlmodel import Column, DateTime, Field, SQLModel, text


class Category(str, Enum):
    INFO = "INFO"
    NEW = "NEW"


class ContentBase(SQLModel):
    title: str = Field(
        ...,
        description="The title of the content",
        min_length=2,
        max_length=200,
    )
    summary: str = Field(
        ...,
        description="A short summary of the content",
        min_length=2,
        max_length=500,
    )
    category: Category = Field(..., description="The category the content belongs to")
    content: str = Field(..., description="The main body/text of the content")
    post_date: datetime = Field(..., description="The date and time when the content was published")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "How to brew the perfect coffee",
                    "summary": "A comprehensive guide to brewing coffee at home.",
                    "category": "INFO",
                    "content": "This is the full text of the content...",
                    "post_date": "2023-10-27T10:00:00",
                }
            ]
        }
    }


class Content(ContentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    embedding: list[float] = Field(sa_column=Column(VECTOR(4096)), exclude=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("now()"),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("now()"),
            onupdate=text("now()"),
            nullable=False,
        ),
    )


class ContentCreate(ContentBase):
    pass


class ContentUpdate(SQLModel):
    title: str | None = None
    summary: str | None = None
    category: Category | None = None
    content: str | None = None
    post_date: datetime | None = None


class ContentRead(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime

