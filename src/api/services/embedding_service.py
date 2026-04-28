import re

from langchain_core.embeddings import Embeddings


class EmbbedingService:
    def __init__(self, emb_model: Embeddings) -> None:
        self.__emb_model = emb_model

    @property
    def emb_model(self) -> Embeddings:
        return self.__emb_model

    async def embed_text(self, text: str) -> list[float]:
        return await self.emb_model.aembed_query(text)

    async def embed_many_texts(self, texts: list[str]) -> list[list[float]]:
        return await self.emb_model.aembed_documents(texts)

    def pre_process_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
        text = re.sub(r"\s+", " ", text).strip()
        return text
