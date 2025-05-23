#  AI-Powered Policy Compliance Checker

This project is a backend-powered AI system that helps users upload policy or legal documents (like PDFs) and analyze them using local LLMs.

Built with:
-  FastAPI
- LLaMA 3.2 via Ollama
-  FAISS for vector search
-  SentenceTransformers for embeddings
-  MongoDB for metadata tracking

---

##  Features

- `/upload/pdf`: Upload a PDF → extract text → chunk and embed it → store vector index and metadata
- `/ask`: Ask questions about the document using vector search + local LLaMA
-  Efficient chunking with overlap to preserve context
-  FAISS index caching (no need to re-embed each time)
-  (Coming Soon) `/check`: Run compliance checks against tags like GDPR, HIPAA, SOC2

---

## Project Structure
rag_local_llama/
├── main.py
├── routers/
│ ├── upload.py
│ └── ask.py
├── services/
│ ├── embedder.py
│ ├── pdf_parser.py
│ ├── vectorstore.py
│ ├── llama_client.py
│ └── db.py
├── data/uploaded_docs/ # Where uploaded PDFs are saved
├── faiss_store/ # Stores per-document FAISS indexes
├── requirements.txt
└── README.md

1. install dependencies

pip install -r requirements.txt

2. Start MongoDB (locally)

mongod --dbpath ~/mongodb/data/db

3.  Start your FastAPI server

uvicorn main:app --reload

Go to: http://localhost:8000/docs

owered by Local LLaMA (via Ollama)
Make sure Ollama is running with the correct model:

ollama run llama3

Ollama should be listening at http://localhost:11434


