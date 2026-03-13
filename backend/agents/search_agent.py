from backend.tools.search_tool import search_restaurants


def search_agent(query):

    results = search_restaurants(query)

    return results