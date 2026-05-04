import pytest
from app.core.chunking import split_text_into_chunks

def test_split_text_into_chunks():
    text = "Đây là một đoạn văn bản mẫu để kiểm tra tính năng cắt nhỏ văn bản. " * 20
    chunk_size = 100
    chunk_overlap = 20
    
    chunks = split_text_into_chunks(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)
    # Kiểm tra xem các đoạn có chứa nội dung không
    assert any("mẫu" in c for c in chunks)

def test_split_text_empty():
    chunks = split_text_into_chunks("", chunk_size=100, chunk_overlap=20)
    assert chunks == []
