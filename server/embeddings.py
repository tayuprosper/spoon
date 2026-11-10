import httpx

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

async def embed(
    input_data: str | list[str], batch_size: int = 16
) -> list[float] | list[list[float]]:
    is_single = isinstance(input_data, str)
    
    # Apply Nomic task prefixes
    if is_single:
        texts = [f"search_query: {input_data}"]
    else:
        texts = [f"search_document: {t}" for t in input_data if t and t.strip()]

    if not texts:
        return [] if not is_single else []

    all_embeddings = []
    async with httpx.AsyncClient(timeout=120.0) as client:
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = await client.post(
                f"{OLLAMA_URL}/api/embed",
                json={"model": EMBED_MODEL, "input": batch},
            )
            response.raise_for_status()
            all_embeddings.extend(response.json()["embeddings"])

    return all_embeddings[0] if is_single else all_embeddings