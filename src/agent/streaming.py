import json
from typing import Literal


class AgentResponseChunk:
    def __init__(
        self,
        content: str,
        type: Literal["text", "error", "info"] = "info",
        done: bool = False,
    ):
        self.content = content
        self.type = type
        self.done = done

    def to_dict(self) -> dict:
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
