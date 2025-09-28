from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument

class PDFQA:
    def __init__(self, text: str):
        self.text = text
        self.vector_store = None
        self.retriever = None
        self.model_name = "BAAI/bge-base-en-v1.5"
        self.embedding_model = HuggingFaceEmbeddings(model_name = self.model_name)
        self._process_pdf()

    def _split_text(self, text: str) -> list[LCDocument]:
        """Hybrid chunking: semantic chunker first, then recursive splitter for finer granularity"""
        # SemanticChunker: captures high-level semantic splits
        semantic_splitter = SemanticChunker(
            embeddings=self.embedding_model,
            buffer_size=4,
            add_start_index=False,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=85,
            number_of_chunks=None,
            sentence_split_regex=r"(?<=[.?!])\s+"
        )
        semantic_docs = semantic_splitter.create_documents([text])

        # RecursiveCharacterTextSplitter: further split large semantic chunks
        final_chunks: list[LCDocument] = []
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,     
            chunk_overlap=150
        )
        for doc in semantic_docs:
            small_chunks = recursive_splitter.split_text(doc.page_content)
            for chunk in small_chunks:
                final_chunks.append(LCDocument(
                    page_content = chunk,
                    metadata = doc.metadata
                ))

        return final_chunks

    def _embed_texts(self, splits: list[LCDocument]) -> FAISS:
        """Embed and create FAISS vector store"""
        vector_store = FAISS.from_documents(splits, self.embedding_model)
        return vector_store

    def _process_pdf(self):
        """Split, embed, create hybrid retriever, and apply reranker"""
        splits = self._split_text(self.text)
        self.vector_store = self._embed_texts(splits)

        # Dense FAISS retriever
        dense_retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 12, "fetch_k": 50, "lambda_mult": 0.7}
        )

        # Sparse BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(splits)

        # Hybrid ensemble retriever
        hybrid_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, dense_retriever],
            weights=[0.35, 0.65]  # adjust weighting as needed
        )

        # Cross-encoder reranker
        cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
        reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=2)

        # Final Contextual Compression Retriever
        self.retriever = ContextualCompressionRetriever(
            base_compressor=reranker,
            base_retriever=hybrid_retriever
        )

def rag_retriever() -> ContextualCompressionRetriever:
    if "pdf_qa" not in st.session_state:
        raise ValueError("⚠️ Please upload and process a PDF first.")
    return st.session_state.pdf_qa.retriever
