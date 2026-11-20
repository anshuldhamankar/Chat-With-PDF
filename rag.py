import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

index = None
chunks = []


def load_pdf(file_bytes: bytes) -> None:
    global index, chunks

    # Extract text
    from io import BytesIO
    reader = PdfReader(BytesIO(file_bytes))
    text = " ".join(page.extract_text() or "" for page in reader.pages)

    # Split into chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    # Embed and build FAISS index
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))


def retrieve(query: str, top_k: int = 3) -> list[str]:
    query_vec = embedder.encode([query], convert_to_numpy=True).astype(np.float32)
    _, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]
