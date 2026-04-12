import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.services.info_service import InfoService
from src.db.models.info import Info, InfoCreate, InfoUpdate


@pytest.fixture
def async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def info_service(async_session):
    return InfoService(async_session)


@pytest.mark.asyncio
async def test_list_info(info_service, async_session):
    mock_info = MagicMock(spec=Info)
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [mock_info]
    async_session.execute.return_value = mock_result

    result = await info_service.list_info()

    assert result == [mock_info]
    async_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_info(info_service, async_session):
    mock_info = MagicMock(spec=Info)
    async_session.get.return_value = mock_info

    result = await info_service.get_info(1)

    assert result == mock_info
    async_session.get.assert_called_with(Info, 1)


@pytest.mark.asyncio
async def test_create_info(info_service, async_session):
    info_data = InfoCreate(title="Test Info", content="Test Content")

    await info_service.create_info(info_data)

    async_session.add.assert_called_once()
    async_session.commit.assert_called_once()
    async_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_info(info_service, async_session):
    mock_info = MagicMock(spec=Info)
    async_session.get.return_value = mock_info
    update_data = InfoUpdate(title="Updated Title")

    result = await info_service.update_info(1, update_data)

    assert result == mock_info
    assert mock_info.title == "Updated Title"
    async_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_info_success(info_service, async_session):
    mock_info = MagicMock(spec=Info)
    async_session.get.return_value = mock_info

    result = await info_service.delete_info(1)

    assert result is True
    async_session.delete.assert_called_with(mock_info)
    async_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_info_not_found(info_service, async_session):
    async_session.get.return_value = None

    result = await info_service.delete_info(1)

    assert result is False
    async_session.delete.assert_not_called()
