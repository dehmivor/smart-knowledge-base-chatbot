from pymilvus import MilvusClient, DataType
from app.config import settings
import uuid

class VectorService:
    def __init__(self):
        # Khởi tạo Milvus Lite (lưu vào file cục bộ)
        self.client = MilvusClient(settings.MILVUS_URI)
        self.collection_name = settings.COLLECTION_NAME
        self._ensure_collection()

    def _ensure_collection(self):
        """Đảm bảo Collection tồn tại trong Milvus"""
        if not self.client.has_collection(self.collection_name):
            # Định nghĩa Schema
            schema = self.client.create_schema(
                auto_id=False,
                enable_dynamic_field=True,
            )
            
            # Thêm các field
            schema.add_field(field_name="id", datatype=DataType.VARCHAR, is_primary=True, max_length=100)
            schema.add_field(field_name="document_id", datatype=DataType.INT64)
            schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1536) # dim=1536 cho OpenAI
            schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
            
            # Cài đặt Index để tìm kiếm nhanh
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="vector",
                index_type="IVF_FLAT",
                metric_type="L2",
                params={"nlist": 128}
            )
            
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )
            print(f"Đã tạo collection: {self.collection_name}")

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
        # Format lại kết quả trả về cho gọn
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
