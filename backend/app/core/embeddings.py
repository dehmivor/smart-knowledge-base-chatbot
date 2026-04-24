from openai import AsyncOpenAI
from app.config import settings
from typing import List

class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Biến danh sách văn bản thành danh sách vectors"""
        if not texts:
            return []
            
        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Lỗi khi gọi OpenAI Embeddings: {e}")
            raise e

embedding_service = EmbeddingService()
