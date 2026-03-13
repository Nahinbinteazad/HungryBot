#!/usr/bin/env python3
"""
Script to precompute embeddings and FAISS index for the food dataset.
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

def _load_dataset(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    entries = [entry.strip() for entry in raw.split("\n\n") if entry.strip()]
    return entries

def main():
    texts = _load_dataset("data/food_dataset.txt")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_numpy=True)
    
    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Create FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    
    # Save index and texts
    faiss.write_index(index, "data/faiss_index.idx")
    with open("data/texts.pkl", "wb") as f:
        pickle.dump(texts, f)
    
    print("Precomputed embeddings and index saved.")

if __name__ == "__main__":
    main()