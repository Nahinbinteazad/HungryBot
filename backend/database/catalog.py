from typing import List, Dict, Optional
from backend.database.vector_store import _load_dataset


def build_index() -> List[Dict[str, str]]:
    """Load dataset into in-memory list for textual search."""
    return _load_dataset('data/food_dataset.txt')


def _matches_filter(item: Dict[str, str], key: str, value: str) -> bool:
    if not value:
        return True
    candidate = item.get(key, '').strip().lower()
    return value.strip().lower() in candidate


def search_catalog(
    query: str = '',
    city: Optional[str] = None,
    cuisine: Optional[str] = None,
    vendor: Optional[str] = None,
    budget: Optional[str] = None,
    subdistrict: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, str]]:
    """Search foods by query + structured filters."""
    catalog = build_index()
    q = query.strip().lower()

    def matches(item: Dict[str, str]) -> bool:
        if city and not _matches_filter(item, 'city', city):
            return False
        if cuisine and not _matches_filter(item, 'cuisine', cuisine):
            return False
        if vendor and not _matches_filter(item, 'vendor', vendor):
            return False
        if budget and not _matches_filter(item, 'budget', budget):
            return False
        if subdistrict and not _matches_filter(item, 'subdistrict', subdistrict):
            return False

        if not q:
            return True

        haystack = ' '.join(
            str(item.get(k, ''))
            for k in ['food', 'place', 'description', 'tags', 'cuisine', 'vendor', 'subdistrict']
        ).lower()
        return q in haystack

    filtered = [item for item in catalog if matches(item)]
    return filtered[:limit]
