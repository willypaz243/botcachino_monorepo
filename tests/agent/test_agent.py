from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agent.agent import UniversityAgent
from src.agent.services import AgentServices


@pytest.fixture
def mock_content_service():
    mock_service = AsyncMock()
    mock_service.search = AsyncMock(return_value=[])
    mock_service.get_by_ids = AsyncMock(return_value=[])
    mock_service.format_content_summary = MagicMock(return_value={"id": 1, "summary": "Test"})
    mock_service.format_content_for_agent = MagicMock(
        return_value={
            "id": 1,
            "title": "Test Title",
            "category": "info",
            "content": "Test content",
            "post_date": "2023-01-01",
        }
    )
    return mock_service


@pytest.fixture
def mock_search_tool():
    mock_tool = AsyncMock()
    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados para la búsqueda.")
    return mock_tool


@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.invoke = MagicMock(return_value=MagicMock(content="off_topic"))
    return mock


@pytest.fixture
def initialized_services(mock_content_service, mock_search_tool):
    AgentServices.initialize(mock_content_service)
    with patch.object(AgentServices, "get_search_tool", return_value=mock_search_tool):
        yield mock_content_service, mock_search_tool
    AgentServices._content_service = None
    AgentServices._search_tool = None


@pytest.mark.asyncio
async def test_agent_initialization(mock_content_service):
    agent = UniversityAgent(mock_content_service)
    assert agent.content_service is mock_content_service
    assert agent._graph is None


@pytest.mark.asyncio
async def test_agent_stream_starts_with_info_event(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        events = []
        async for event in agent.astream_events("Hello", "thread-1"):
            events.append(event)
            if event.get("done"):
                break

    assert len(events) > 0
    assert events[0]["event"] == "info"
    assert "Iniciando" in events[0]["content"]


@pytest.mark.asyncio
async def test_agent_stream_yields_multiple_events(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    events = []
    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        async for event in agent.astream_events("Hello", "thread-1"):
            events.append(event)

    assert len(events) >= 2


@pytest.mark.asyncio
async def test_agent_invoke_returns_dict(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        result = await agent.invoke("Hello", "thread-1")

    assert isinstance(result, dict)
    assert "response" in result
    assert "sources" in result


@pytest.mark.asyncio
async def test_agent_invoke_returns_sources_list(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        result = await agent.invoke("Hello", "thread-1")

    assert isinstance(result["sources"], list)


@pytest.mark.asyncio
async def test_agent_invoke_returns_response_string(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        result = await agent.invoke("Hello", "thread-1")

    assert isinstance(result["response"], str)


@pytest.mark.asyncio
async def test_agent_stream_all_events_have_required_fields(initialized_services, mock_llm):
    mock_service, mock_tool = initialized_services
    agent = UniversityAgent(mock_service)

    mock_tool.ainvoke = AsyncMock(return_value="No se encontraron resultados.")

    with patch("langchain_nebius.ChatNebius", return_value=mock_llm):
        async for event in agent.astream_events("Hello", "thread-1"):
            assert "event" in event
            assert "content" in event
            if event.get("done"):
                break
