import os
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGRetriever:
    """
    Handles chunking, embedding, and retrieval over the math difficulty rubric.
    """
    def __init__(self, doc_path: str = "math_difficulty_rubric.txt", max_words: int = 20000):
        # Load the rubric text
        text = Path(doc_path).read_text(encoding="utf-8")
        # Chunk into ~max_words-per‐chunk
        self.chunks = self._chunk_text(text, max_words)
        # Initialize embedding model
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        # Embed all chunks
        embeddings = self.embed_model.encode(self.chunks, convert_to_numpy=True)
        # Build a FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def _chunk_text(self, text: str, max_words: int):
        words = text.split()
        return [
            " ".join(words[i : i + max_words])
            for i in range(0, len(words), max_words)
        ]

    def retrieve(self, query: str, k: int = 5):
        """
        Returns the top-k most relevant rubric chunks for the given query.
        """
        # Encode the query
        q_emb = self.embed_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb, k)
        return [self.chunks[i] for i in indices[0]]