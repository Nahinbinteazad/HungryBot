from typing import List, Tuple
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer


class FAISSVectorStore:
    """A vector store using precomputed FAISS index for semantic retrieval."""

    def __init__(self, index_path: str, texts_path: str):
        self.index = faiss.read_index(index_path)
        with open(texts_path, "rb") as f:
            self.texts = pickle.load(f)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, k)
        results = [(self.texts[idx], float(score)) for idx, score in zip(indices[0], scores[0])]
        return results


def _load_dataset(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    entries = [entry.strip() for entry in raw.split("\n\n") if entry.strip()]
    return entries


def create_vector_store():
    return FAISSVectorStore("data/faiss_index.idx", "data/texts.pkl")


def get_food_list():
    """Return a list of food names found in the dataset."""

    foods = []
    for entry in _load_dataset("data/food_dataset.txt"):
        for line in entry.splitlines():
            if line.lower().startswith("food:"):
                foods.append(line.split(":", 1)[1].strip())
                break
    return foods


vector_db = create_vector_store()
