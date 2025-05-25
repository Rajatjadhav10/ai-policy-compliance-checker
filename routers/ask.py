from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.pdf_parser import extract_text_from_pdf, chunk_text
from services.embedder import Embedder
from services.vectorstore import VectorStore
from services.db import get_document_by_id
from services.llama_client import ask_llama
import os

router = APIRouter()

class AskRequest(BaseModel):
    document_id: str
    question: str

@router.post("/")
def ask_question(payload: AskRequest):
    doc = get_document_by_id(payload.document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    filename = doc["filename"]
    pdf_path = os.path.join("data/uploaded_docs", f"{payload.document_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")

    index_path = os.path.join("faiss_store", f"{payload.document_id}.index")
    dimension = 384  
    vectorstore = VectorStore(dimension, index_path=index_path)

# If index doesn't exist, return error
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Vector index not found. Please upload the document first.")
    # 1. Re-extract and chunk
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    # 2. Embed chunks
    embedder = Embedder()
    embeddings = embedder.embed(chunks)

    # 3. Build FAISS and search
    dimension = embeddings[0].shape[0]
    vectorstore = VectorStore(dimension)
    vectorstore.add_embeddings(embeddings)

    query_embedding = embedder.embed([payload.question])[0]
    indices, _ = vectorstore.search(query_embedding, k=5)

    # 4. Collect top-k context
    top_chunks = [chunks[i] for i in indices[0]]

    # 5. Send to LLaMA
    answer = ask_llama(payload.question, top_chunks)

    return {
        "document_id": payload.document_id,
        "question": payload.question,
        "answer": answer,
        "top_chunks": top_chunks
    }
