from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings

class LocalEmbeddings(Embeddings):

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts)

    def embed_query(self, text):
        return self.model.encode(text)


def create_vector_store():

    loader = TextLoader("data/food_dataset.txt")
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = LocalEmbeddings()

    db = FAISS.from_documents(split_docs, embeddings)

    return db


vector_db = create_vector_store()