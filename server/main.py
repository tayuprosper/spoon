import os
import uuid
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pdf_utils import extract_text
from chunking import chunk_text
from embeddings import embed
from vectorstore import add_chunks, search
import rag


# Create FastAPI app instance
app = FastAPI()

# Allow cross-origin requests from the client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class AskRequest(BaseModel):
    question: str
    doc_id: str | None = None  # optional: restrict search to one document

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    print("[1] Upload started...", flush=True)
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    doc_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    print(f"[2] File saved to {save_path}", flush=True)

    try:
        print("[3] Extracting text...", flush=True)
        text = extract_text(save_path)
        print(f"[3.1] Extracted {len(text)} characters", flush=True)

        print("[4] Chunking text...", flush=True)
        chunks = chunk_text(text)
        print(f"[4.1] Generated {len(chunks)} chunks", flush=True)

        if not chunks:
            raise HTTPException(status_code=422, detail="No extractable text found in PDF.")

        print("[5] Embedding chunks...", flush=True)
        # CRITICAL: Ensure 'await' is used if embed is async
        embeddings = await embed(chunks) 
        print(f"[5.1] Generated {len(embeddings)} embeddings", flush=True)

        print("[6] Saving to vector store...", flush=True)
        add_chunks(doc_id=doc_id, chunks=chunks, embeddings=embeddings)
        print("[7] Ingestion complete!", flush=True)

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR EXCEPTION]: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return {"doc_id": doc_id, "chunks_indexed": len(chunks)}

@app.post("/ask")
async def ask(req: AskRequest):
    """Answer a question using the RAG pipeline (retrieve context → generate answer)."""
    try:
        query_embedding =await embed(req.question)
        top_chunks = search(query_embedding, top_k=5, doc_id=req.doc_id)
        if not top_chunks:
            return {"answer": "No relevant context found. Please upload a document first."}
        answer = rag.ask(req.question, top_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"answer": answer}


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}