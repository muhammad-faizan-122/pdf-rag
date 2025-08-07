import logging
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from main.constants import PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL


class VectorStoreBuilder:
    def __init__(self, embedding_model=EMBEDDING_MODEL):
        self.embedding = OllamaEmbeddings(model=embedding_model)

    def create_vector_db(self, chunks):
        vector_db = Chroma.from_documents(
            persist_directory=PERSIST_DIR,
            documents=chunks,
            embedding=self.embedding,
            collection_name=COLLECTION_NAME,
        )
        logging.info("Vector DB created successfully.")
        return vector_db
