import urllib.parse

from backend.agents.food_agent import food_agent
from backend.tools.search_tool import search_restaurants
from backend.database.vector_store import get_food_list


def search_agent(query):
    """Return chat-style responses for location/restaurant queries."""

    q = query.lower().strip()

    # If the user asks what the bot knows, list all foods in the dataset
    if any(phrase in q for phrase in ["what do you know", "what can you do", "what foods"]):
        foods = get_food_list()
        if not foods:
            return "I don't have any food knowledge yet."
        return "I know about these Bangladeshi foods:\n" + "\n".join(f"- {f}" for f in foods)

    # Provide a map link + food info for food location questions
    for food in get_food_list():
        if food.lower() in q:
            term = f"{food} in Bangladesh"
            maps_link = "https://www.google.com/maps/search/" + urllib.parse.quote_plus(term)
            info = food_agent(food).strip()

            response = [f"Here’s what I know about {food}:\n\n{info}"]
            response.append(f"\nTo find restaurants, try this map search:\n{maps_link}")
            response.append(
                f"\nYou can also search for '{food} restaurant in Chattogram' on Google Maps for exact addresses."
            )
            return "\n".join(response)

    # Fallback to web search when no built-in answer is available
    return search_restaurants(query)
