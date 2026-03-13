from backend.agents.food_agent import food_agent
from backend.agents.search_agent import search_agent
from backend.agents.ocr_agent import ocr_agent


def route_query(query, image=None):

    # If an image is uploaded -> use OCR agent
    if image is not None:
        return ocr_agent(image)

    query_lower = query.lower()

    # If asking about restaurants
    if "restaurant" in query_lower or "where" in query_lower:
        return search_agent(query)

    # Otherwise use food knowledge
    return food_agent(query)