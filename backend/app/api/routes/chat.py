from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.rag_pipeline import rag_pipeline

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatSource(BaseModel):
    text: str
    filename: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource]

@router.post("/", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Tin nhắn không được để trống")
    
    try:
        result = await rag_pipeline.generate_answer(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống Chat: {str(e)}")
