import json
import os
import numpy as np
from embeddings import embed_text

STORE_PATH = "./vector_store.json"


def _load_store() -> list[dict]:
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, "r") as f:
            return json.load(f)
    return []


def _save_store(store: list[dict]):
    with open(STORE_PATH, "w") as f:
        json.dump(store, f)


def add_chunks(doc_id: str, chunks: list[str], embeddings: list[list[float]]):
    store = _load_store()
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        store.append(
            {
                "id": f"{doc_id}-{i}",
                "doc_id": doc_id,
                "text": chunk,
                "embedding": embedding,
            }
        )

    _save_store(store)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search(query_embedding: list[float], top_k: int = 3, doc_id: str | None = None) -> list[str]:
    store = _load_store()
    if doc_id:
        store = [item for item in store if item["doc_id"] == doc_id]

    scored = [
        (cosine_similarity(query_embedding, item["embedding"]), item["text"])
        for item in store
    ]

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scored[:top_k]]