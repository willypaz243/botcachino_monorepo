import json
from typing import Any, Literal


class AgentResponseChunk:
    def __init__(
        self,
        content: str,
        type: Literal["text", "error", "info"] = "info",
        done: bool = False,
    ) -> None:
        self.content: str = content
        self.type: Literal["text", "error", "info"] = type
        self.done: bool = done

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "type": self.type,
            "done": self.done,
        }

    def to_sse(self) -> bytes:
        return f"data: {json.dumps(self.to_dict())}\n\n".encode()


def format_sse(
    content: str,
    type: Literal["text", "error", "info"] = "info",
    done: bool = False,
) -> bytes:
    chunk = AgentResponseChunk(content=content, type=type, done=done)
    return chunk.to_sse()
