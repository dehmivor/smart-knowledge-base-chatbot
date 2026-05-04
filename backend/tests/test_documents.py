import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import os
import time

@pytest.fixture
def mock_services():
    with patch("app.api.routes.documents.embedding_service") as mock_embed, \
         patch("app.api.routes.documents.vector_service") as mock_vector, \
         patch("app.api.routes.documents.extract_text_from_file", new_callable=AsyncMock) as mock_extract:
        
        mock_embed.get_embeddings = AsyncMock(return_value=[[0.1] * 1536])
        mock_extract.return_value = "Nội dung văn bản giả lập để test"
        mock_vector.insert_chunks.return_value = 1
        
        yield {
            "embed": mock_embed,
            "vector": mock_vector,
            "extract": mock_extract
        }

def test_upload_documents_invalid_type(client):
    files = [
        ("files", ("test.exe", b"binary data", "application/x-msdownload"))
    ]
    response = client.post("/api/v1/documents/upload", files=files)
    assert response.status_code == 400
    assert "Không có file hợp lệ" in response.json()["detail"]

def test_list_documents_empty(client):
    response = client.get("/api/v1/documents/")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_document_success(client, mock_services):
    file_content = b"Hello testing world"
    files = [
        ("files", ("test_upload.txt", file_content, "text/plain"))
    ]
    
    response = client.post("/api/v1/documents/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "test_upload.txt"
    
    # Kiểm tra đúng hàm con được gọi
    mock_services["extract"].assert_called_once()
    mock_services["embed"].get_embeddings.assert_called_once()
    
    # Dọn dẹp file với retry
    upload_path = os.path.join("uploads", "test_upload.txt")
    for _ in range(5):
        try:
            if os.path.exists(upload_path):
                os.remove(upload_path)
            break
        except Exception:
            time.sleep(0.1)
