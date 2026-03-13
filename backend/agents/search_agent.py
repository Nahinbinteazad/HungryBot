from backend.tools.search_tool import search_restaurants


def search_agent(query):
    """Return chat-style responses for location/restaurant queries."""

    q = query.lower().strip()

    # Quick, built-in guidance for popular Bangladeshi foods
    if "mezban" in q:
        return (
            "Mezban is a traditional feast-style cuisine from Chattogram. "
            "For Mezban Beef, look for "
            "restaurants and community "
            "\"mezban\" halls in the Patenga/Agrabad area of Chattogram. "
            "Popular names include Anowara Mezban, Chattogram Mezban Center, "
            "and local village mezbans (often held as community events). "
            "To find exact locations, search for \"Mezban restaurant in Chattogram\" "
            "on Google Maps or follow the links below."
        )

    if "fuchka" in q or "panipuri" in q:
        return (
            "Fuchka (panipuri) is a beloved street snack in Dhaka and Chattogram. "
            "In Chattogram, you can find it near Patenga Beach, city markets, "
            "and busy food streets. Try searching for 'best fuchka in Chattogram' "
            "on map apps to find the closest stalls."
        )

    return search_restaurants(query)
