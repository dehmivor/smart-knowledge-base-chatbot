from unstructured.partition.auto import partition

async def extract_text_from_file(file_path: str) -> str:
    """Trích xuất chữ từ đường dẫn file PDF, DOCX, TXT..."""
    # Dùng thư viện unstructured để tự động nhận diện và đọc file từ đường dẫn
    elements = partition(filename=file_path)
    
    # Ghép các đoạn text lại với nhau
    text = "\n\n".join([str(el) for el in elements])
    return text
