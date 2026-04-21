from unstructured.partition.auto import partition
import io

async def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Trích xuất chữ từ file PDF, DOCX, TXT..."""
    # Dùng thư viện unstructured để tự động nhận diện và đọc file
    file_obj = io.BytesIO(file_content)
    elements = partition(file=file_obj, filename=filename)
    
    # Ghép các đoạn text lại với nhau
    text = "\n\n".join([str(el) for el in elements])
    return text
