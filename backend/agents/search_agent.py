import urllib.parse

from backend.agents.food_agent import food_agent
from backend.tools.search_tool import search_restaurants
from backend.tools.places_api import search_openstreetmap, search_google_places
from backend.database.catalog import search_catalog
from backend.database.vector_store import get_food_list, get_city_foods, get_city_restaurants


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
        rating = rec.get('rating', 'N/A')
        tags = rec.get('tags', '')

        line = f"- {food} ({typ}) · Rating: {rating}"
        if tags:
            line += f" · Tags: {tags}"
        lines.append(line + f"\n  Where: {place}\n  Info: {desc}\n")
    return "\n".join(lines)


def _format_catalog_search_results(records):
    if not records:
        return None

    lines = [f"Catalog found {len(records)} matching entries:\n"]
    for rec in records:
        food = rec.get('food', 'Unknown food')
        place = rec.get('place', 'Local eateries')
        typ = rec.get('type', 'restaurant')
        desc = rec.get('description', '')
        rating = rec.get('rating', 'N/A')
        tags = rec.get('tags', '')

        line = f"- {food} ({typ}) · Rating: {rating}"
        if tags:
            line += f" · Tags: {tags}"
        lines.append(line + f"\n  Where: {place}\n  Info: {desc}\n")

    return "\n".join(lines)


def _format_city_grocery_suggestions(city, records):
    if not records:
        return None

    lines = [f"Grocery and ingredient spots in {city.title()}:\n"]
    for rec in records:
        food = rec.get('food', 'Unknown item')
        place = rec.get('place', 'Local market')
        typ = rec.get('type', 'grocery')
        desc = rec.get('description', '')
        rating = rec.get('rating', 'N/A')
        tags = rec.get('tags', '')

        line = f"- {food} ({typ}) · Rating: {rating}"
        if tags:
            line += f" · Tags: {tags}"
        lines.append(line + f"\n  Where: {place}\n  Info: {desc}\n")
    return "\n".join(lines)


def search_agent(query):
    """Return chat-style responses for location/restaurant queries."""

    q = query.lower().strip()

    # If the user asks a city-specific query, suggest city restaurant/street-food specials.
    city_keywords = {
        'dhaka': 'Dhaka',
        'chattogram': 'Chattogram',
        'chittagong': 'Chattogram',
        'sylhet': 'Sylhet',
        "cox's bazar": "Cox's Bazar",
        'cox bazar': 'Cox\'s Bazar'
    }

    for token, city_name in city_keywords.items():
        if token in q and any(w in q for w in ['where', 'famous', 'best', 'special', 'recommend', 'eat']):
            city_records = get_city_restaurants(city_name)
            city_response = _format_city_food_suggestions(city_name, city_records)
            if city_response:
                maps_link = "https://www.google.com/maps/search/" + urllib.parse.quote_plus(f"{city_name} restaurants food")
                city_response += f"\nFind these places on maps: {maps_link}\n"
                city_response += "\nTip: include the food name + city on Google Maps, e.g., 'Kacchi Biryani Dhaka'."
                return city_response

            # fallback to catalog search if structured food list is missing
            catalog_results = search_catalog(query='', city=city_name, limit=12)
            catalog_response = _format_catalog_search_results(catalog_results)
            if catalog_response:
                catalog_response += "\nTip: ask for budget/food category to narrow results."
                return catalog_response

            # fallback to OpenStreetMap search
            osm_results = search_openstreetmap(f"restaurants {city_name}", city_name, limit=5)
            if osm_results:
                lines = [f"I couldn't find enough local database entries for {city_name}, but here are nearby places from OpenStreetMap:" , ""]
                for r in osm_results:
                    lines.append(f"- {r.get('name')} ({r.get('type')})\n  {r.get('link')}")
                return "\n".join(lines)

    # If the user asks a city-specific grocery query, politely redirect to restaurant mode
    if any(w in q for w in ['grocery', 'buy', 'market', 'supermarket', 'ingredient']):
        return "This app focuses on restaurant and street food recommendations. Please ask about a city (e.g., Dhaka, Chattogram, Sylhet, Cox's Bazar) and dishes you want to eat."

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
