from langchain_text_splitters import RecursiveCharacterTextSplitter
# (Chỉ cần đổi dấu . thành dấu _)

def split_text_into_chunks(text: str, chunk_size: 500, chunk_overlap: 50):
    """Chia nhỏ văn bản thành các đoạn 500 chữ, gối đầu nhau 50 chữ"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks
