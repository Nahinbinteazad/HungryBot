from backend.database.vector_store import vector_db


def food_agent(query):

    docs = vector_db.similarity_search(query, k=3)

    response = ""

    for d in docs:
        response += d.page_content + "\n"

    return response