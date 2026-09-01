# 📖 The Restricted Archive — Harry Potter RAG

A Retrieval-Augmented Generation (RAG) system that answers questions about the Harry Potter books using **only** the content of the books themselves. Ask about a character, a spell, an object, or an event, and the system retrieves the most relevant passages from a vector database before generating a grounded answer — no hallucinated lore, no outside knowledge.

![The Restricted Archive — demo screenshot](./demo-screenshot.png)

## How it works, in one screenshot

The two red boxes above are the whole interaction, end to end:

1. **Red box on the left — ask the archive.** You type a question in the text area and press **Consult the Archive** (or `Ctrl + Enter`). The frontend sends that question to the FastAPI backend.
2. **Behind the scenes.** The backend embeds your question, searches **ChromaDB** for the book passages ("chunks") whose meaning is closest to it, and passes those retrieved chunks — along with your question — to an LLM (via Groq) with strict instructions to answer *only* from that retrieved context.
3. **Red box on the right — the archive replies.** The generated answer streams back into the result panel, grounded entirely in the chunks that were actually retrieved from the books.

If the retrieved chunks don't contain enough information to answer, the model says so instead of making something up.

## Architecture

```
┌──────────────┐      question       ┌──────────────────┐
│              │ ──────────────────▶ │                   │
│   Frontend   │                     │   FastAPI backend │
│ (HTML/CSS/JS)│ ◀────────────────── │                   │
└──────────────┘      answer         └─────────┬─────────┘
                                                 │
                          ┌──────────────────────┼──────────────────────┐
                          ▼                      ▼                      ▼
                 ┌────────────────┐   ┌────────────────────┐  ┌─────────────────┐
                 │  QueryRouter    │   │     Retriever       │  │ AnswerGenerator │
                 │ (classify the   │   │ (embed question →   │  │ (LLM answers    │
                 │  question as    │   │  search ChromaDB     │  │  using only the │
                 │  retrieve /     │   │  for matching        │  │  retrieved      │
                 │  chitchat /     │   │  book chunks)         │  │  chunks)        │
                 │  off-topic)     │   └──────────┬───────────┘  └────────┬────────┘
                 └────────────────┘              │                        │
                                                   ▼                        ▼
                                          ┌─────────────────┐      ┌────────────────┐
                                          │    ChromaDB      │      │   Groq LLM API  │
                                          │ (harry_potter_   │      │  (llama / etc.) │
                                          │  pages collection)│      └────────────────┘
                                          └──────────────────┘
```

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, vanilla JavaScript (single self-contained page, no build step) |
| Backend | FastAPI (Python) |
| Vector store | ChromaDB |
| Embeddings | `intfloat/multilingual-e5-large` (Sentence Transformers) |
| Query classification | Groq LLM |
| Answer generation | Groq LLM (via `langchain-groq`) |

## Project structure

```
backend/
├── .env
├── app/
│   ├── main.py                  # FastAPI app, CORS, routes
│   ├── api/
│   │   └── routes/
│   │       └── query.py         # POST /query/ endpoint
│   └── services/
│       ├── router.py            # QueryRouter — classifies the question
│       ├── retrieval.py         # Retriever — embeds + searches ChromaDB
│       └── generator.py         # AnswerGenerator — builds the final answer
└── data/
    └── vector_store/
        └── chroma_data/         # Persisted ChromaDB collection

frontend/
└── index.html                   # The Restricted Archive UI
```

## Getting started

### 1. Backend

**Requirements:** Python 3.12, a CUDA-capable GPU (the embedding model loads with `device="cuda"`), and a [Groq](https://console.groq.com) API key.

```bash
cd backend
pip install -r requirements.txt   # fastapi, uvicorn, chromadb, sentence-transformers, langchain-groq, python-dotenv, etc.
```

Create a `.env` file in `backend/`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

Run the API:

```bash
uvicorn app.main:app --reload
```

The API will start on `http://127.0.0.1:8000`. On first boot it loads the embedding model and connects to the existing ChromaDB collection — check the terminal for a `Chunks: <n>` log confirming the book data is loaded.

### 2. Frontend

The frontend is a single static file with no dependencies or build step.

```bash
cd frontend
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser, confirm the API endpoint field points to `http://127.0.0.1:8000`, and press **Ping API** — a green dot means the backend is reachable.

> You can also just double-click `index.html` to open it directly as a local file; CORS is already open (`allow_origins=["*"]`) on the backend.

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Basic status message |
| `GET` | `/health` | Health check — `{"status": "healthy"}` |
| `POST` | `/query/` | Submit a question, receive a book-grounded answer |

## Example questions

- *What is a Horcrux?*
- *Who is Sirius Black?*
- *What is the Triwizard Tournament?*
- *What does the Marauder's Map do?*

## Notes

- Answers are only as good as the retrieved chunks — always worth cross-checking against the source pages, which is why the UI footer says exactly that.
- Questions unrelated to the books are classified as `off-topic` or `chitchat` by the `QueryRouter` before any retrieval happens, keeping irrelevant queries from hitting the vector store.
