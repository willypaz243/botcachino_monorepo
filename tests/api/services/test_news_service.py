import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.services.news_service import NewsService
from src.db.models.news import News, NewsCreate, NewsUpdate


@pytest.fixture
def async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def news_service(async_session):
    return NewsService(async_session)


@pytest.mark.asyncio
async def test_list_news(news_service, async_session):
    mock_news = MagicMock(spec=News)
    mock_result = MagicMock()
    mock_result.scalars().all.return_value = [mock_news]
    async_session.execute.return_value = mock_result

    result = await news_service.list_news()

    assert result == [mock_news]
    async_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_news(news_service, async_session):
    mock_news = MagicMock(spec=News)
    async_session.get.return_value = mock_news

    result = await news_service.get_news(1)

    assert result == mock_news
    async_session.get.assert_called_with(News, 1)


@pytest.mark.asyncio
async def test_create_news(news_service, async_session):
    news_data = NewsCreate(title="Test News", content="Test Content")

    await news_service.create_news(news_data)

    async_session.add.assert_called_once()
    async_session.commit.assert_called_once()
    async_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_news(news_service, async_session):
    mock_news = MagicMock(spec=News)
    async_session.get.return_value = mock_news
    update_data = NewsUpdate(title="Updated Title")

    result = await news_service.update_news(1, update_data)

    assert result == mock_news
    assert mock_news.title == "Updated Title"
    async_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_news_success(news_service, async_session):
    mock_news = MagicMock(spec=News)
    async_session.get.return_value = mock_news

    result = await news_service.delete_news(1)

    assert result is True
    async_session.delete.assert_called_with(mock_news)
    async_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_news_not_found(news_service, async_session):
    async_session.get.return_value = None

    result = await news_service.delete_news(1)

    assert result is False
    async_session.delete.assert_not_called()
