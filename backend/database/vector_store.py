from typing import List, Tuple, Dict
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


def _load_dataset(path: str) -> List[Dict[str, str]]:
    """Load dataset entries where each block is parsed into a key/value dict."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    blocks = [block.strip() for block in raw.split("\n\n") if block.strip()]
    entries = []
    for block in blocks:
        item = {}
        for line in block.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                item[key.strip().lower()] = value.strip()
        if item:
            entries.append(item)
    return entries


def create_vector_store():
    return FAISSVectorStore("data/faiss_index.idx", "data/texts.pkl")


def get_food_list() -> List[str]:
    """Return a list of food names found in the dataset."""
    foods = []
    for item in _load_dataset("data/food_dataset.txt"):
        if 'food' in item and item['food']:
            foods.append(item['food'])
    return foods


def get_city_foods(city: str) -> List[Dict[str, str]]:
    """Return all dish records for a given city."""
    city_lower = city.strip().lower()
    return [item for item in _load_dataset("data/food_dataset.txt") if item.get('city', '').strip().lower() == city_lower]


vector_db = create_vector_store()
