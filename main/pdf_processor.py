import logging
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def load_and_split(self, pdf_path):
        logging.info(f"Loading PDF from: {pdf_path}")
        loader = PDFMinerLoader(pdf_path)
        data = loader.load()
        logging.info(f"Loaded {len(data)} document(s).")

        chunks = self.text_splitter.split_documents(data)
        logging.info(f"Split into {len(chunks)} chunks.")
        return chunks
