import requests

LLAMA_ENDPOINT = "http://localhost:11434/api/generate"

PROMPT_TEMPLATE = """
You are a compliance assistant helping a company check and understand the content of internal policy or legal documents.

Your goal is to identify key policy mentions, flag missing requirements, and provide clear answers based strictly on the document content.

Below is an excerpt from the document:
{context}

Question:
{question}

Be concise and specific. Only use the provided content. If the answer is not found, say "Not mentioned in the document."

Answer:
"""

def ask_llama(question, context_chunks):
    context = "\n".join(context_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(LLAMA_ENDPOINT, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error from LLaMA API: {response.status_code} - {response.text}"
