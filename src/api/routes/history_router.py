from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_history_service
from src.api.routes.schemas import PaginationParams
from src.api.services.history_service import HistoryService
from src.db.models.history import (
    ConversationCreate,
    ConversationRead,
    ConversationUpdate,
    MessageCreate,
    MessageRead,
)

router = APIRouter(prefix="/history", tags=["History"])

@router.post(
    "/conversations/",
    response_model=ConversationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    conversation_in: ConversationCreate,
    history_service: HistoryService = Depends(get_history_service),
):
    """Create a new conversation."""
    return await history_service.create_conversation(conversation_in)


@router.get("/conversations/", response_model=list[ConversationRead])
async def read_conversations(
    limit: int = PaginationParams.limit,
    offset: int = PaginationParams.offset,
    history_service: HistoryService = Depends(get_history_service),
):
    """Retrieve all conversations (paginated)."""
    return await history_service.get_all_conversations(limit=limit, offset=offset)


@router.get("/conversations/{uuid}", response_model=ConversationRead)
async def read_conversation(
    uuid: str,
    history_service: HistoryService = Depends(get_history_service),
):
    """Retrieve a single conversation by UUID (includes its messages)."""
    conversation = await history_service.get_conversation_by_uuid(uuid)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.patch("/conversations/{uuid}", response_model=ConversationRead)
async def update_conversation(
    uuid: str,
    conversation_in: ConversationUpdate,
    history_service: HistoryService = Depends(get_history_service),
):
    """Update a conversation's title."""
    conversation = await history_service.update_conversation(uuid, conversation_in)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    uuid: str,
    history_service: HistoryService = Depends(get_history_service),
):
    """Delete a conversation and all its messages (cascade)."""
    success = await history_service.delete_conversation(uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None

@router.post(
    "/conversations/{uuid}/messages/",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    uuid: str,
    message_in: MessageCreate,
    history_service: HistoryService = Depends(get_history_service),
):
    """Add a message to an existing conversation."""
    message = await history_service.add_message(uuid, message_in)
    if not message:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return message


@router.get("/conversations/{uuid}/messages/", response_model=list[MessageRead])
async def read_messages(
    uuid: str,
    limit: int = PaginationParams.limit,
    offset: int = PaginationParams.offset,
    history_service: HistoryService = Depends(get_history_service),
):
    """Retrieve all messages for a conversation (ordered by timestamp)."""
    return await history_service.get_messages(uuid, limit=limit, offset=offset)


@router.delete(
    "/conversations/{uuid}/messages/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_messages(
    uuid: str,
    history_service: HistoryService = Depends(get_history_service),
):
    """Delete all messages from a conversation without deleting the conversation."""
    success = await history_service.clear_conversation_messages(uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    history_service: HistoryService = Depends(get_history_service),
):
    """Delete a single message by ID."""
    success = await history_service.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return None