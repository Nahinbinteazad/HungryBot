import urllib.parse

from backend.agents.food_agent import food_agent
from backend.tools.search_tool import search_restaurants
from backend.database.vector_store import get_food_list, get_city_foods


def _format_city_food_suggestions(city, records):
    in_city = [rec for rec in records if rec.get('city', '').strip()]
    if not in_city:
        return None

    lines = [f"Top {len(in_city)} specialties for {city.title()}:\n"]
    for rec in in_city:
        food = rec.get('food', 'Unknown food')
        place = rec.get('place', 'Local eateries')
        typ = rec.get('type', 'restaurant')
        desc = rec.get('description', '')

        lines.append(f"- {food} ({typ})\n  Where: {place}\n  Info: {desc}\n")
    return "\n".join(lines)


def search_agent(query):
    """Return chat-style responses for location/restaurant queries."""

    q = query.lower().strip()

    # If the user asks a city-specific query, suggest city best dishes/grocery
    city_keywords = {
        'dhaka': 'Dhaka',
        'chattogram': 'Chattogram',
        'chittagong': 'Chattogram',
        'sylhet': 'Sylhet',
        "cox's bazar": "Cox's Bazar",
        'cox bazar': 'Cox\'s Bazar'
    }
    for token, city_name in city_keywords.items():
        if token in q and any(w in q for w in ['where', 'famous', 'best', 'special', 'recommend', 'grocery', 'buy']):
            city_records = get_city_foods(city_name)
            city_response = _format_city_food_suggestions(city_name, city_records)
            if city_response:
                maps_link = "https://www.google.com/maps/search/" + urllib.parse.quote_plus(f"{city_name} food")
                city_response += f"\nFind these places on maps: {maps_link}\n"
                city_response += "\nTip: include the food name + city on Google Maps, e.g., 'Kacchi Biryani Dhaka'."
                return city_response

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

    # If this looks like a location/restaurants query, try a generic map search.
    if any(kw in q for kw in ["where", "restaurant", "location", "located"]):
        maps_link = "https://www.google.com/maps/search/" + urllib.parse.quote_plus(q)
        return (
            "I couldn't find a specific place in my local knowledge, but you can try this map search:\n"
            f"{maps_link}\n\n"
            "You can also refine your question with a specific food name (e.g., 'Where can I eat Kacchi Biryani?')."
        )

    # Fallback to web search when no built-in answer is available
    return search_restaurants(query)
