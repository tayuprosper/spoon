def chunk_text(text: str, chunck_size: int = 300, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunck_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunck_size - overlap
    return chunks

