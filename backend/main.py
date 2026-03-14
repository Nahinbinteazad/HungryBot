from langsmith import traceable

# agents
from backend.agents.food_agent import food_agent

# tools
from backend.tools.search_tool import search_restaurants
from backend.tools.ocr_tool import classify_food_image

# database
from backend.database.vector_store import get_food_list


@traceable(name="route_query")
def route_query(query, image=None):

    # IMAGE CASE
    if image is not None:
        foods = get_food_list()
        result = classify_food_image(image, foods)

        if not result:
            return "I could not recognize the food."

        return "I think this might be:\n" + "\n".join(result)

    query_lower = query.lower().strip()

    # FOOD LIST
    if any(kw in query_lower for kw in ["what foods", "food list", "what do you know"]):
        foods = get_food_list()

        if not foods:
            return "I don't know any foods yet."

        return "I know these Bangladeshi foods:\n" + "\n".join(foods)

    # RESTAURANT SEARCH
    if "restaurant" in query_lower or "where" in query_lower:
        return search_restaurants(query)

    # DEFAULT → FOOD KNOWLEDGE
    return food_agent(query)