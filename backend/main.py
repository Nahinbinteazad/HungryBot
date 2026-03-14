from backend.agents.food_agent import food_agent
from backend.agents.search_agent import search_agent
from backend.agents.ocr_agent import ocr_agent
from backend.database.vector_store import get_food_list


def route_query(query, image=None):

    # If an image is uploaded -> use OCR agent
    if image is not None:
        return ocr_agent(image)

    query_lower = query.lower().strip()

    # If the user asks what the bot knows
    if any(kw in query_lower for kw in ["what do you know", "what can you do", "what foods"]):
        foods = get_food_list()
        if not foods:
            return "I don't know any foods yet."
        return "I know about these Bangladeshi foods:\n" + "\n".join(f"- {f}" for f in foods)

    # If asking about restaurants or city-specific famous foods
    if "restaurant" in query_lower or "where" in query_lower or any(city in query_lower for city in ["dhaka", "chattogram", "sylhet", "cox", "cox's bazar"]):
        return search_agent(query)

    # Otherwise use food knowledge
    return food_agent(query)