This project is a simple, fully local implementation of a Retrieval-Augmented Generation (RAG) system. It lets you ask questions over any PDF document using:

- PDF text extraction via PyMuPDF
- Embedding generation via `sentence-transformers`
- FAISS vector search
- Local LLaMA 3.2 1B (via [Ollama](https://ollama.com/)) for answer generation

##  How It Works

1. Loads and chunks a PDF into small text segments
2. Converts them to embeddings and stores in a FAISS index
3. Accepts a user question and retrieves the top-3 relevant chunks
4. Builds a prompt and sends it to your **local LLaMA model** via Ollama
5. Prints the answer

##  Requirements

```bash
pip install -r requirements.txt