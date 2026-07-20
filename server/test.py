import asyncio
from pdf_utils import extract_text
from chunking import chunk_text
from embeddings import embed_text, embed_texts
from vectorstore import add_chunks, search
from rag import ask

# Ingest (skip if vector_store.json already has this doc indexed)
text = extract_text("test.pdf")
chunks = chunk_text(text)
chunk_embeddings = asyncio.run(embed_texts(chunks))  # concurrent — much faster than looping embed_text()
add_chunks(doc_id="test-doc", chunks=chunks, embeddings=chunk_embeddings)

# Ask
question = "What is redis"
query_embedding = embed_text(question)
top_chunks = search(query_embedding, top_k=3)
print("--- Retrieved chunks ---")
for i, c in enumerate(top_chunks):
    print(f"\nChunk {i+1}:\n{c}")
answer = ask(question, top_chunks)
print(answer)