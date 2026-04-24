from app.core.embeddings import embedding_service
from app.services.vector_service import vector_service
from app.config import settings
from openai import AsyncOpenAI

class RAGPipeline:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.CHAT_MODEL

    async def generate_answer(self, query: str):
        # 1. Biến câu hỏi thành Vector
        query_vector = (await embedding_service.get_embeddings([query]))[0]
        
        # 2. Tìm kiếm các đoạn văn bản liên quan trong Milvus
        relevant_docs = vector_service.search_similar(query_vector, limit=5)
        
        if not relevant_docs:
            return {
                "answer": "Xin lỗi, tôi không tìm thấy thông tin liên quan trong tài liệu của bạn.",
                "sources": []
            }

        # 3. Xây dựng Context từ các đoạn văn bản tìm được
        context_text = "\n\n".join([
            f"--- Nguồn: {doc['filename']} ---\n{doc['text']}" 
            for doc in relevant_docs
        ])

        # 4. Tạo Prompt cho AI
        system_prompt = f"""
Bạn là một trợ lý AI thông minh chuyên tra cứu tài liệu nội bộ công ty.
Hãy sử dụng thông tin trong phần CONTEXT dưới đây để trả lời câu hỏi của người dùng.
Nếu trong CONTEXT không có thông tin, hãy lịch sự nói rằng bạn không biết, đừng tự bịa ra câu trả lời.
Luôn trả lời bằng ngôn ngữ mà người dùng đang hỏi (mặc định là tiếng Việt).

CONTEXT:
{context_text}
"""

        # 5. Gọi OpenAI GPT để trả lời
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.3 # Độ sáng tạo thấp để đảm bảo tính chính xác
            )
            
            return {
                "answer": response.choices[0].message.content,
                "sources": relevant_docs
            }
        except Exception as e:
            print(f"Lỗi khi gọi OpenAI Chat: {e}")
            raise e

rag_pipeline = RAGPipeline()
