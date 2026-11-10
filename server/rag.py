import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

# The rest of your ask() function remains exactly the same"
CHAT_MODEL = "phi4-mini"
PROMPT_TEMPLATE = """Context:
{context}

Question: {question}

Instructions:
- Answer the question based ONLY on the context provided above.
- If the answer is not mentioned in the context, respond with: "I couldn't find that in the document."
- If the context contains a list, list every item line by line.

Answer:"""


def ask(question: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    
    # Temporarily print the final prompt string
    print(context_chunks)
    
    response = httpx.post(
        "http://localhost:11434/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,  # Use 0.0 for deterministic factual extraction
                "num_ctx": 4096      # Ensure context window is large enough for 3 full chunks
            }
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"]
    