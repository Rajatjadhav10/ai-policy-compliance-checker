import faiss
import numpy as np
import os

class VectorStore:
    def __init__(self, dimension, index_path=None):
        self.dimension = dimension
        self.index_path = index_path

        if index_path and os.path.exists(index_path):
            print(f"[FAISS] Loading existing index from: {index_path}")
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)

    def search(self, query_embedding, k=5):
        query = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query, k)
        return indices, distances

    def save(self):
        if self.index_path:
            faiss.write_index(self.index, self.index_path)
