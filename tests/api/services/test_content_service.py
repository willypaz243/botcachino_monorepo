from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.content_service import ContentService
from src.db.models.content import Category, Content, ContentCreate, ContentUpdate


@pytest.mark.asyncio
async def test_create_content():
    session = AsyncMock(spec=AsyncSession)
    content_in = ContentCreate(
        title="Test Title",
        summary="Test Summary",
        category=Category.INFO,
        content="Test Content",
        post_date=datetime.fromisoformat("2023-01-01T00:00:00"),
    )

    service = ContentService(session)
    result = await service.create_content(content_in)

    assert result.title == "Test Title"
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_contents():
    session = AsyncMock(spec=AsyncSession)
    mock_content = MagicMock(spec=Content)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_content]
    session.execute.return_value = mock_result

    service = ContentService(session)
    result = await service.get_all_contents()

    assert len(result) == 1
    assert result[0] == mock_content


@pytest.mark.asyncio
async def test_get_content_by_id():
    session = AsyncMock(spec=AsyncSession)
    mock_content = MagicMock(spec=Content)
    session.get.return_value = mock_content

    service = ContentService(session)
    result = await service.get_content_by_id(1)

    assert result == mock_content
    session.get.assert_called_with(Content, 1)


@pytest.mark.asyncio
async def test_get_content_by_id_not_found():
    session = AsyncMock(spec=AsyncSession)
    session.get.return_value = None

    service = ContentService(session)
    result = await service.get_content_by_id(1)

    assert result is None


@pytest.mark.asyncio
async def test_update_content_success():
    session = AsyncMock(spec=AsyncSession)
    mock_content = MagicMock(spec=Content)
    session.get.return_value = mock_content

    content_in = ContentUpdate(
        title="Updated Title",
        summary="Updated Summary",
        category=Category.NEW,
        content="Updated Content",
        post_date=datetime.fromisoformat("2023-01-01T00:00:00"),
    )

    service = ContentService(session)
    result = await service.update_content(1, content_in)

    assert result == mock_content
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_content_not_found():
    session = AsyncMock(spec=AsyncSession)
    session.get.return_value = None

    content_in = ContentUpdate(title="Updated Title")

    service = ContentService(session)
    result = await service.update_content(1, content_in)

    assert result is None


@pytest.mark.asyncio
async def test_delete_content_success():
    session = AsyncMock(spec=AsyncSession)
    mock_content = MagicMock(spec=Content)
    session.get.return_value = mock_content

    service = ContentService(session)
    result = await service.delete_content(1)

    assert result is True
    session.delete.assert_called_once_with(mock_content)
    session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_content_not_found():
    session = AsyncMock(spec=AsyncSession)
    session.get.return_value = None

    service = ContentService(session)
    result = await service.delete_content(1)

    assert result is False
