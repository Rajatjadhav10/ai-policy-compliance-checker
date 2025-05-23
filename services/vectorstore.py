import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        self.index.add(np.array(embeddings))

    def search(self, query_embedding, k=5):
        query = np.array([query_embedding])
        distances, indices = self.index.search(query, k)
        return indices, distances