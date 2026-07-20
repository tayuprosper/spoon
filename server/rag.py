import httpx

OLLAMA_URL = "http://localhost:11434"
CHAT_MODEL = "llama3.2"

PROMPT_TEMPLATE = """You are a document Q&A assistant. Answer the question using ONLY the context below.

Rules:
- If the answer is not contained in the context, say "I couldn't find that in the document."
- Do not use outside knowledge, even if you know the answer.
- If the context contains a list or enumeration relevant to the question, copy out every single item from that list, in order, one per line. Missing any item is a failure. Do not stop until you have transcribed the entire list.
- Be concise otherwise.

Context:
{context}

Question: {question}

Answer:"""


def ask(question: str, context_chuncks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chuncks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    # print("=== FULL PROMPT SENT ===")
    # print(prompt)
    # print("=== END PROMPT ===")
    response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 500}
        },
        timeout=120,
    )
    response.raise_for_status()
    # data = response.json()
    # print("done_reason:", data.get("done_reason"))
    # print("eval_count:", data.get("eval_count"))
    # print("full response:\n", data["response"])
    return response.json()["response"]
