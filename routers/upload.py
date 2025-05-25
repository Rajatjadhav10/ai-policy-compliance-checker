from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from services.pdf_parser import extract_text_from_pdf, chunk_text
from services.embedder import Embedder
from services.vectorstore import VectorStore
from services.db import save_document_metadata

router = APIRouter()
UPLOAD_DIR = "data/uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # 1. Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    
   

    # 3. Extract and chunk text
    text = extract_text_from_pdf(file.file)
    chunks = chunk_text(text)

    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks could be extracted from the document")


    

    # 4. Embed chunks
    embedder = Embedder()
    embeddings = embedder.embed(chunks)

    

    # 5. Build FAISS index (in-memory for now)
    dimension = embeddings[0].shape[0]
    vectorstore = VectorStore(dimension)
    vectorstore.add_embeddings(embeddings)

    # Save FAISS index
    


    # 6. Save metadata in MongoDB
    document_id = save_document_metadata(file.filename, len(chunks))
    pdf_path = os.path.join(UPLOAD_DIR, f"{document_id}.pdf")

    index_path = os.path.join("faiss_store", f"{document_id}.index")
    vectorstore.index_path = index_path
    vectorstore.save()

    # 5. Save the PDF file to disk
    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    # 7. Return success response
    return {
        "document_id": document_id,
        "filename": file.filename,
        "chunks": len(chunks)
    }
