from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os

from app.core.document_loader import extract_text_from_file
from app.core.chunking import split_text_into_chunks
from app.core.embeddings import embedding_service
from app.services.vector_service import vector_service
from app.models.database import get_db, DocumentMetadata
from app.models.schemas import DocumentResponse
from app.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ PDF, DOCX hoặc TXT")

    try:
        # Đọc nội dung file
        content = await file.read()
        
        # Lưu file vật lý vào thư mục uploads (Optional nhưng tốt cho quản lý)
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)

        # Trích xuất text và chunking (Sử dụng đường dẫn file đã lưu)
        text = await extract_text_from_file(file_path)
        chunks = split_text_into_chunks(text, chunk_size=500, chunk_overlap=50)
        
        # --- PHASE 2: EMBEDDING & VECTOR DB ---
        # 1. Gọi OpenAI tạo embeddings cho các chunks
        vectors = await embedding_service.get_embeddings(chunks)
        
        # 2. Lưu metadata vào SQLite trước để lấy document_id
        new_doc = DocumentMetadata(
            filename=file.filename,
            file_type=file.content_type,
            chunk_count=len(chunks)
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        # 3. Lưu vectors vào Milvus
        vector_service.insert_chunks(
            document_id=new_doc.id,
            chunks=chunks,
            vectors=vectors,
            filename=file.filename
        )
        # --------------------------------------
        
        return new_doc
        
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentMetadata).all()
    return docs

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return doc

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    
    # Xóa file vật lý
    file_path = os.path.join(settings.UPLOAD_DIR, doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # Xóa vectors trong Milvus
    vector_service.delete_by_document_id(document_id)
        
    # Xóa trong DB
    db.delete(doc)
    db.commit()
    
    return {"message": f"Đã xóa tài liệu {doc.filename}"}

