def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Splits text into ~1000 character chunks with a 200 character overlap."""
    cleaned_text = " ".join(text.split())  # Normalize whitespace & newlines
    if not cleaned_text:
        return []

    chunks = []
    start = 0
    text_len = len(cleaned_text)
    stride = chunk_size - overlap

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = cleaned_text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += stride

    return chunks