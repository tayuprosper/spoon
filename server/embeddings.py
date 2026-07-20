import asyncio
import httpx

OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"


def embed_text(text: str) -> list[float]:
    """Embed a single string (synchronous, used for query embedding)."""
    response = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["embedding"]


async def _embed_one(client: httpx.AsyncClient, text: str) -> list[float]:
    response = await client.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
    )
    response.raise_for_status()
    return response.json()["embedding"]


async def embed_texts(texts: list[str], max_concurrent: int = 8) -> list[list[float]]:
    """Embed a list of strings concurrently — much faster than looping embed_text().
    Use `await embed_texts(chunks)` inside async contexts (FastAPI).
    Use `asyncio.run(embed_texts(chunks))` in plain scripts.
    max_concurrent caps the number of in-flight requests to avoid PoolTimeout.
    """
    sem = asyncio.Semaphore(max_concurrent)

    async def _guarded(client: httpx.AsyncClient, text: str) -> list[float]:
        async with sem:
            return await _embed_one(client, text)

    async with httpx.AsyncClient(timeout=60) as client:
        return await asyncio.gather(*[_guarded(client, t) for t in texts])