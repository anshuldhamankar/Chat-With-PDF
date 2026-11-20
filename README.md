# Chat with PDF

A RAG-based application that lets you upload a PDF and ask questions about its content using Google Gemini and FAISS.

## How It Works

1. Upload a PDF → text is extracted, split into 500-char chunks, and embedded using `sentence-transformers`
2. Embeddings are stored in a FAISS vector index in memory
3. On each question, the top-3 most relevant chunks are retrieved and sent as context to Gemini
4. The answer is returned and saved to a SQLite database

## Project Structure

```
PythonProject/
├── main.py              # FastAPI app, endpoints
├── rag.py               # PDF loading, chunking, FAISS indexing & retrieval
├── db.py                # SQLite chat history
├── requirements.txt
├── .env                 # GEMINI_API_KEY goes here
└── templates/
    └── index.html       # Chat UI
```

## Setup

**1. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key to `.env`**
```env
GEMINI_API_KEY=your-gemini-api-key
```
Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

**4. Run the server**
```bash
python -m uvicorn main:app --reload
```

**5. Open in browser**
```
http://localhost:8000
```

## API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | Chat UI                            |
| POST   | `/upload`  | Upload and index a PDF             |
| POST   | `/chat`    | Ask a question about the PDF       |
| GET    | `/history` | Retrieve last 20 questions/answers |

## Tech Stack

| Component       | Library                  |
|-----------------|--------------------------|
| API Framework   | FastAPI                  |
| LLM             | Google Gemini (`gemini-2.5-flash-lite`) |
| Vector Store    | FAISS                    |
| Embeddings      | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| PDF Parsing     | pypdf                    |
| Chat History    | SQLite                   |
