from duckduckgo_search import DDGS


def search_restaurants(query):

    results_text = ""

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

        for r in results:
            results_text += f"{r['title']}\n{r['href']}\n\n"

    return results_text