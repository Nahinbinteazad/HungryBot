import os
import requests
from typing import Optional
from urllib.parse import quote_plus


def search_google_places(query: str, city: str = '', api_key: Optional[str] = None, limit: int = 5):
    """Search Google Places Text Search (requires API key)."""
    if api_key is None:
        api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if api_key is None:
            raise ValueError('Google Places API key not set (GOOGLE_PLACES_API_KEY)')

    full_query = f"{query} {city}".strip()
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={quote_plus(full_query)}&key={api_key}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get('status') != 'OK':
        return []

    results = []
    for item in data.get('results', [])[:limit]:
        results.append({
            'name': item.get('name'),
            'address': item.get('formatted_address'),
            'rating': item.get('rating'),
            'types': item.get('types'),
            'place_id': item.get('place_id'),
            'url': f"https://www.google.com/maps/place/?q=place_id:{item.get('place_id')}"
        })
    return results


def search_openstreetmap(query: str, city: str = '', limit: int = 5):
    """Search OpenStreetMap Nominatim for restaurants."""
    full_query = f"{query} {city}".strip()
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': full_query,
        'format': 'json',
        'limit': limit,
        'addressdetails': 1,
    }
    headers = {
        'User-Agent': 'HungryBot/1.0 (you@example.com)'
    }
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = []
    for item in data:
        results.append({
            'name': item.get('display_name'),
            'lat': item.get('lat'),
            'lon': item.get('lon'),
            'type': item.get('type'),
            'class': item.get('class'),
            'link': f"https://www.openstreetmap.org/?mlat={item.get('lat')}&mlon={item.get('lon')}#map=18/{item.get('lat')}/{item.get('lon')}"
        })
    return results
