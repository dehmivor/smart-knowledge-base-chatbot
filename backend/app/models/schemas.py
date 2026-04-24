from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    chunk_count: int
    upload_date: datetime

    class Config:
        from_attributes = True

class HealthCheck(BaseModel):
    status: str
    version: str = "1.0.0"
