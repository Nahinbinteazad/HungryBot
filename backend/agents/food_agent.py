from backend.database.vector_store import vector_db


def food_agent(query):

    docs = vector_db.similarity_search(query, k=3)

    response = ""

    for doc_text, distance in docs:
        response += f"{doc_text}\n\n"

    return response