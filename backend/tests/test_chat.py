import pytest
from unittest.mock import patch, AsyncMock

@pytest.fixture
def mock_rag():
    # Sử dụng AsyncMock vì generate_answer là hàm bất đồng bộ
    with patch("app.api.routes.chat.rag_pipeline") as mock_pipeline:
        mock_pipeline.generate_answer = AsyncMock(return_value={
            "answer": "Đây là câu trả lời giả lập từ AI.",
            "sources": [
                {"text": "Đoạn văn bản nguồn...", "filename": "doc1.pdf", "score": 0.9}
            ]
        })
        yield mock_pipeline

def test_chat_empty_message(client):
    response = client.post("/api/v1/chat/", json={"message": ""})
    assert response.status_code == 400
    assert "không được để trống" in response.json()["detail"]

def test_chat_success(client, mock_rag):
    response = client.post("/api/v1/chat/", json={"message": "Công ty ở đâu?"})
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "Đây là câu trả lời giả lập từ AI."
    assert len(data["sources"]) == 1
    
    mock_rag.generate_answer.assert_called_once_with("Công ty ở đâu?")
