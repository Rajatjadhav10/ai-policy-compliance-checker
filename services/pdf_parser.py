import fitz

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