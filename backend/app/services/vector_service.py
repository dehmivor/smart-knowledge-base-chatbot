from pymilvus import MilvusClient, DataType
from app.config import settings
import uuid

class VectorService:
    def __init__(self):
        # Khởi tạo lười: không tạo client ngay lập tức
        self._client = None
        self.collection_name = settings.COLLECTION_NAME

    @property
    def client(self):
        """Tự động khởi tạo client khi được gọi tới lần đầu"""
        if self._client is None:
            self._client = MilvusClient(settings.MILVUS_URI)
            self._ensure_collection()
        return self._client

    def _ensure_collection(self):
        """Đảm bảo Collection tồn tại trong Milvus"""
        # Dùng self._client trực tiếp để tránh vòng lặp đệ quy
        if not self._client.has_collection(self.collection_name):
            schema = self._client.create_schema(
                auto_id=False,
                enable_dynamic_field=True,
            )
            
            schema.add_field(field_name="id", datatype=DataType.VARCHAR, is_primary=True, max_length=100)
            schema.add_field(field_name="document_id", datatype=DataType.INT64)
            schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1536)
            schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
            
            index_params = self._client.prepare_index_params()
            index_params.add_index(
                field_name="vector",
                index_type="IVF_FLAT",
                metric_type="L2",
                params={"nlist": 128}
            )
            
            self._client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )

    def insert_chunks(self, document_id: int, chunks: list, vectors: list, filename: str):
        """Chèn các đoạn văn bản và vectors vào Milvus"""
        data = []
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            data.append({
                "id": str(uuid.uuid4()),
                "document_id": document_id,
                "vector": vector,
                "text": chunk,
                "filename": filename,
                "chunk_index": i
            })
        
        self.client.insert(collection_name=self.collection_name, data=data)
        return len(data)

    def delete_by_document_id(self, document_id: int):
        """Xóa toàn bộ vector thuộc về một tài liệu"""
        self.client.delete(
            collection_name=self.collection_name,
            filter=f"document_id == {document_id}"
        )

    def search_similar(self, query_vector: list, limit: int = 5):
        """Tìm kiếm các đoạn văn bản có vector gần giống nhất với câu hỏi"""
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=limit,
            output_fields=["text", "filename", "document_id"]
        )
        formatted_results = []
        if results and len(results) > 0:
            for res in results[0]:
                formatted_results.append({
                    "text": res["entity"]["text"],
                    "filename": res["entity"]["filename"],
                    "score": res["distance"]
                })
        return formatted_results

vector_service = VectorService()
