from fastapi import APIRouter, UploadFile, File, HTTPException, Depends # Thêm Depends
from sqlalchemy.orm import Session
from app.core.document_loader import extract_text_from_file
from app.core.chunking import split_text_into_chunks
from app.models.database import get_db, DocumentMetadata # Thêm dòng này

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)): # Thêm db param
    allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ PDF, DOCX hoặc TXT")

    try:
        content = await file.read()
        text = await extract_text_from_file(content, file.filename)
        chunks = split_text_into_chunks(text)
        
        # --- LƯU METADATA VÀO SQLITE ---
        new_doc = DocumentMetadata(
            filename=file.filename,
            file_type=file.content_type,
            chunk_count=len(chunks)
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        # -------------------------------
        
        return {
            "id": new_doc.id, # Trả về ID mới tạo
            "filename": file.filename,
            "chunk_count": len(chunks),
            "upload_date": new_doc.upload_date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")

# Thêm API lấy danh sách file đã upload để chứng minh bạn làm việc với DB tốt
@router.get("/")
async def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentMetadata).all()
    return docs
