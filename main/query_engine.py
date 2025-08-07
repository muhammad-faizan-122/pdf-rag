import logging
from langchain import hub
from langchain_ollama.chat_models import ChatOllama
from main.constants import LLM_MODEL


class QueryEngine:
    def __init__(self, model=LLM_MODEL):
        self.llm = ChatOllama(model=model)
        self.prompt = hub.pull("rlm/rag-prompt")

    def get_answer(self, vector_db, query):
        logging.info(f"Received query: {query}")
        docs = vector_db.similarity_search(query, k=2)
        logging.info(f"Retrieved {len(docs)} document(s).")

        context = "\n\n".join([doc.page_content for doc in docs])
        messages = self.prompt.invoke(
            {"context": context, "question": query}
        ).to_messages()

        response = self.llm.invoke(messages)
        logging.info("LLM response generated.")
        return response.content
