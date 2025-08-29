from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers import ContextualCompressionRetriever
import streamlit as st

class PDFQA:
    def __init__(self, text: str):
        self.text = text
        self.vector_store = None
        self.retriever = None
        self._process_pdf()

    def _split_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.create_documents([text])

    def _embed_texts(self, splits):
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(splits, embedding)
        return vector_store

    def _process_pdf(self):
        splits = self._split_text(self.text)
        self.vector_store = self._embed_texts(splits)

        # build retriever right here
        base_retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 7, "fetch_k": 30}
        )
        model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
        reranker = CrossEncoderReranker(model=model, top_n=5)
        self.retriever = ContextualCompressionRetriever(
            base_compressor=reranker,
            base_retriever=base_retriever
        )


def rag_retriever() -> ContextualCompressionRetriever:
    if "pdf_qa" not in st.session_state:
        raise ValueError("⚠️ Please upload and process a PDF first.")
    return st.session_state.pdf_qa.retriever
    
        