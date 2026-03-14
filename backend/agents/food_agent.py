from backend.database.vector_store import create_vector_store
from langsmith import traceable

# load vector database
vector_db = create_vector_store()


@traceable(name="food_agent")
def food_agent(query):

    docs = vector_db.similarity_search(query, k=3)

    response = ""

    for text, score in docs:
        response += f"{text}\n\n"

    if response == "":
        return "Sorry, I couldn't find information about that food."

    return response