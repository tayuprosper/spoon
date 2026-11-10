import json
import os
import numpy as np
from embeddings import embed

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
    print(f"[DEBUG] Total store entries: {len(store)}")
    
    if doc_id:
        store = [item for item in store if item["doc_id"] == doc_id]
        print(f"[DEBUG] Entries after filtering by doc_id='{doc_id}': {len(store)}")

    if not store:
        print("[DEBUG] WARNING: Vector store is empty! Check doc_id or JSON loading.")
        return []

    scored = [
        (cosine_similarity(query_embedding, item["embedding"]), item["text"])
        for item in store
    ]

    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Print top retrieval scores
    for score, text in scored[:top_k]:
        print(f"[DEBUG] Score: {score:.4f} | Excerpt: {text[:60]}...")

    return [text for _, text in scored[:top_k]]