import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class SimpleVectorStore:
    def __init__(self, texts: List[str]):
        self.texts = texts
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        vectors = self.model.encode(self.texts, convert_to_numpy=True)
        self.dimension = vectors.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(vectors)

    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.texts):
                continue
            results.append((self.texts[idx], float(dist)))
        return results


def _load_dataset(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read().strip()

    entries = [entry.strip() for entry in raw.split('\n\n') if entry.strip()]
    return entries


def create_vector_store():
    texts = _load_dataset('data/food_dataset.txt')
    return SimpleVectorStore(texts)


vector_db = create_vector_store()
