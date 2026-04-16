from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from src.agent import UniversityAgent
from src.agent.streaming import format_sse
from src.api.dependencies import get_content_service
from src.api.services.content_service import ContentService

router = APIRouter(prefix="/agent", tags=["agent"])


async def get_agent(
    content_service: ContentService = Depends(get_content_service),
) -> UniversityAgent:
    return UniversityAgent(content_service)


@router.post("/chat")
async def chat_with_agent(
    message: str = Query(
        ...,
        title="Message",
        description="The message to send to the agent",
        min_length=1,
        max_length=2000,
    ),
    thread_id: str = Query(
        ...,
        title="Thread ID",
        description="Unique identifier for the conversation thread",
        min_length=1,
        max_length=100,
    ),
    agent: UniversityAgent = Depends(get_agent),
) -> StreamingResponse:
    """Chat with the university information agent.

    Uses Server-Sent Events (SSE) for streaming responses.
    Each event follows the AgentResponseChunk format.
    """

    async def event_generator():
        try:
            async for event in agent.astream_events(
                message=message,
                thread_id=thread_id,
            ):
                event_type = event.get("event", "info")
                content = event.get("content", "")
                done = event_type == "done"

                yield format_sse(
                    content=content,
                    type=event_type if event_type != "done" else "info",
                    done=done,
                )

        except Exception as e:
            yield format_sse(
                content=f"Error inesperado: {str(e)}",
                type="error",
            )
            yield format_sse(content="", type="info", done=True)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
