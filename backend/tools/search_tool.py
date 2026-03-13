from duckduckgo_search import DDGS


def search_restaurants(query):
    """Search the web and return a friendly, chat-style summary."""

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

    if not results:
        return "Sorry, I couldn't find any results for that query."

    response_lines = [
        "Here are a few places and resources I found:",
        "",
    ]

    for i, r in enumerate(results, start=1):
        title = r.get("title") or "(No title)"
        href = r.get("href") or "(No URL)"
        snippet = (r.get("body") or "").strip().replace("\n", " ")
        if snippet and len(snippet) > 200:
            snippet = snippet[:197].rstrip() + "..."

        response_lines.append(f"{i}. {title}\n   {href}")
        if snippet:
            response_lines.append(f"   {snippet}")
        response_lines.append("")

    response_lines.append(
        "Tip: click a link to see exact location details, or refine your question for a more specific recommendation."
    )

    return "\n".join(response_lines)