import fitz  # PyMuPDF
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests

# 1. Load and chunk PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return " ".join([page.get_text() for page in doc])

def chunk_text(text, chunk_size=300):
    sentences = text.split('.')
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + '.'
        else:
            chunks.append(current.strip())
            current = sentence + '.'
    chunks.append(current.strip())
    return chunks

# 2. Embed and index
def build_faiss_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, model, chunks

# 3. Retrieve top-k chunks
def search_chunks(query, model, index, chunks, k=3):
    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector), k)
    return [chunks[i] for i in I[0]]

# 4. Build prompt
def build_prompt(retrieved_chunks, query):
    prompt = "Use the following information to answer the question , if the information is not available in the context, say so:\n\n"
    for i, chunk in enumerate(retrieved_chunks):
        prompt += f"Context {i+1}:\n{chunk}\n\n"
    prompt += f"Question: {query}\nAnswer:"
    return prompt

# 5. Send to LLaMA via Ollama locally
def ask_llama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2:1b", "prompt": prompt, "stream": False}
    )
    print("Status Code:", response.status_code)
    try:
        return response.json()["response"]
    except:
        return "Error: LLaMA did not return valid response."

# 6. Run it all
def run_rag(pdf_path, question):
    print(" Loading and chunking PDF...")
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    print(f" Created {len(chunks)} chunks")

    print("🔍 Building index...")
    index, model, all_chunks = build_faiss_index(chunks)

    print(" Searching for relevant context...")
    top_chunks = search_chunks(question, model, index, all_chunks)

    print(" Building prompt and asking LLaMA...")
    prompt = build_prompt(top_chunks, question)
    answer = ask_llama(prompt)

    print("\n Final Answer:\n", answer)

# Run this
if __name__ == "__main__":
    run_rag("your_notes.pdf", "What is virtual memory?")