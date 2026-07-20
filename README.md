# ✦ Spoon

**Spoon** is a local-first, privacy-focused PDF chat application. Upload any PDF and ask questions about it — answers are grounded exclusively in the document's content using a Retrieval-Augmented Generation (RAG) pipeline powered entirely by [Ollama](https://ollama.com) (no external APIs, no data leaves your machine).

---

## How It Works

1. **Upload** a PDF via the Next.js frontend.
2. The **FastAPI backend** extracts text, splits it into chunks, and embeds each chunk using the `nomic-embed-text` model via Ollama.
3. Embeddings are stored in an in-memory/JSON **vector store**.
4. When you ask a question, the backend **retrieves** the most relevant chunks (cosine similarity) and passes them as context to the `llama3.2` model.
5. The model answers using **only** the retrieved document content.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 (React 19, TypeScript) |
| Backend | FastAPI (Python) |
| Embeddings | `nomic-embed-text` via Ollama |
| LLM | `llama3.2` via Ollama |
| PDF parsing | `pdfminer` / `pypdf` |

---

## Prerequisites

Make sure the following are installed before you begin:

- **Node.js** v18+ and **npm**
- **Python** 3.11+
- **[Ollama](https://ollama.com)** — running locally on port `11434`

### Pull the required Ollama models

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Verify Ollama is running:

```bash
ollama list
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd spoon
```

---

### 2. Start the Backend (FastAPI)

```bash
cd server
```

**Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

**Install dependencies:**

```bash
pip install fastapi uvicorn httpx pdfminer.six pypdf
```

**Start the server:**

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

> **Note:** Uploaded PDFs are saved to the `server/uploads/` directory. The vector store is persisted to `server/vector_store.json`.

---

### 3. Start the Frontend (Next.js)

Open a new terminal tab:

```bash
cd client
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

---

## Environment Variables

By default, the frontend points to `http://localhost:8000` for the API. To override this (e.g. for a deployed backend), create a `.env.local` file in the `client/` directory:

```env
# client/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Project Structure

```
spoon/
├── client/                  # Next.js frontend
│   ├── app/
│   │   ├── page.tsx         # Home / upload page
│   │   └── chat/[docId]/
│   │       └── page.tsx     # Chat page (per document)
│   └── lib/
│       └── api.ts           # API client (upload, ask)
│
└── server/                  # FastAPI backend
    ├── main.py              # API routes (/upload, /ask)
    ├── pdf_utils.py         # PDF text extraction
    ├── chunking.py          # Text chunking logic
    ├── embeddings.py        # Ollama embedding calls
    ├── vectorstore.py       # Vector store (add, search)
    └── rag.py               # RAG prompt + LLM call
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a PDF file. Returns `doc_id` and `chunks_indexed`. |
| `POST` | `/ask`    | Ask a question. Body: `{ "question": "...", "doc_id": "..." }` |

---

## Usage

1. Open `http://localhost:3000` in your browser.
2. Drop or select a PDF file and click **Upload**.
3. Once processing is complete, you'll be redirected to the chat interface.
4. Type your question and press **Enter** — the assistant answers using only the document's content.
5. Press **+ New document** to upload another PDF.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused` on upload | Make sure `uvicorn` is running on port `8000` |
| `model not found` error | Run `ollama pull nomic-embed-text` and `ollama pull llama3.2` |
| Ollama not responding | Check Ollama is running: `ollama serve` |
| No text extracted from PDF | The PDF may be image-only (scanned). OCR is not supported yet. |
| CORS errors in browser | Ensure the backend is started and `allow_origins=["*"]` is set in `main.py` |

---

## License

MIT
