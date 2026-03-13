from typing import List, Tuple


class SimpleVectorStore:
    """A lightweight keyword-based retrieval store.

    This avoids downloading large embedding models, so it works quickly
    on Streamlit Community Cloud.
    """

    def __init__(self, texts: List[str]):
        self.texts = texts

    def similarity_search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        # Score each document by how many query words it contains.
        query_tokens = [t.lower() for t in query.split() if t.strip()]
        scores = []

        for doc in self.texts:
            doc_lower = doc.lower()
            score = sum(1 for t in query_tokens if t in doc_lower)
            scores.append((doc, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [(doc, float(score)) for doc, score in scores[:k]]


def _load_dataset(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()

    entries = [entry.strip() for entry in raw.split("\n\n") if entry.strip()]
    return entries


def create_vector_store():
    texts = _load_dataset("data/food_dataset.txt")
    return SimpleVectorStore(texts)


vector_db = create_vector_store()
