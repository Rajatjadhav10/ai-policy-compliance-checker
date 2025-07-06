# AI-Powered Policy Compliance Checker

This project is an AI-driven backend system designed to analyze and evaluate policy or legal documents (PDFs) using local large language models (LLMs). It enables document uploads, semantic search, and (coming soon) compliance tagging—all while running fully offline.

## Tech Stack

- **FastAPI** – Backend API framework  
- **LLaMA 3.2 via Ollama** – Local language model  
- **FAISS** – Vector similarity search for document retrieval  
- **SentenceTransformers** – Text embedding  
- **MongoDB** – Stores document metadata and processing info  

---

## Key Features

- `POST /upload/pdf`  
  Upload a PDF → Extract → Chunk → Embed → Save FAISS index and metadata

- `POST /ask`  
  Ask a question about a document. Uses semantic search + local LLaMA for answer generation

- Chunking with context-preserving overlap for improved retrieval

- FAISS index caching: avoids redundant embedding for the same document

- `POST /check` (Coming Soon)  
  Perform rule-based compliance checks (GDPR, HIPAA, SOC2, etc.)

---





