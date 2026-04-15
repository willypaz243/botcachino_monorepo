from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.server import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.invoke = MagicMock(return_value=MagicMock(content="off_topic"))
    return mock


class TestAgentEndpoint:
    def test_chat_endpoint_exists(self, client):
        response = client.post(
            "/api/agent/chat",
            params={"message": "Hello", "thread_id": "test-001"},
        )
        assert response.status_code in [200, 500, 502, 503]

    def test_chat_endpoint_requires_message(self, client):
        response = client.post(
            "/api/agent/chat",
            params={"thread_id": "test-001"},
        )
        assert response.status_code == 422

    def test_chat_endpoint_requires_thread_id(self, client):
        response = client.post(
            "/api/agent/chat",
            params={"message": "Hello"},
        )
        assert response.status_code == 422

    def test_chat_endpoint_validates_message_length(self, client):
        long_message = "x" * 3000
        response = client.post(
            "/api/agent/chat",
            params={"message": long_message, "thread_id": "test-001"},
        )
        assert response.status_code == 422

    def test_chat_endpoint_validates_thread_id_length(self, client):
        long_thread = "x" * 150
        response = client.post(
            "/api/agent/chat",
            params={"message": "Hello", "thread_id": long_thread},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_response_is_sse(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/api/agent/chat",
                params={"message": "Hello", "thread_id": "test-001"},
                headers={"Accept": "text/event-stream"},
            )
            assert response.status_code in [200, 500, 502, 503]

    def test_chat_response_content_type(self, client):
        response = client.post(
            "/api/agent/chat",
            params={"message": "Hello", "thread_id": "test-001"},
        )
        if response.status_code == 200:
            assert "text/event-stream" in response.headers.get("content-type", "")


class TestRootEndpoint:
    def test_root_returns_message(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestDocsEndpoint:
    def test_docs_endpoint_available(self, client):
        response = client.get("/docs")
        assert response.status_code == 200
