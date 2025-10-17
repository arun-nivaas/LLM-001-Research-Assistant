import logging
from services.rag_pipeline import PDFQA
from llm_client_rag import get_llm_client_rag 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from const import Constants
from langsmith import Client
from config import settings


# Initialize Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# LangSmith Client
client = Client(api_key = settings.LANGSMITH_API_KEY)
rag_prompt = client.pull_prompt("research_bot_rag_prompt", include_model=False)


# Conversational Memory
memory = ConversationBufferMemory(
    memory_key = Constants.CHAT_HISTORY,
    return_messages = True,
    output_key = Constants.ANSWER
) 

# RAG Service Class
class RAGService:
    def __init__(self):
        self.qa_chain = None 
        self.pdf_qa = None

    def process_pdf(self, extract_text:str, token:str):

        pdf_qa = PDFQA(extract_text)

        try:
            llm = get_llm_client_rag(token)
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=pdf_qa.retriever,
                return_source_documents=True,
                combine_docs_chain_kwargs = {"prompt": rag_prompt},
                memory = memory,
                verbose=False,
                output_key = Constants.ANSWER
            )

        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {e}")
            raise

        self.pdf_qa = pdf_qa
        self.qa_chain = qa_chain

    def query(self, user_query: str):

        logger.info(f"Query received: {user_query}")

        if not self.qa_chain:
            raise ValueError("RAG pipeline not initialized. Upload a PDF first.")
        try:
            result = self.qa_chain.invoke({"question": user_query})
            answer = result.get("answer") or result.get("result") or str(result)
            sources = [doc.page_content[:350] for doc in result.get("source_documents", [])] if "source_documents" in result else []
            return answer, sources
        
        except Exception as e:
            logger.error(f"Error during query processing: {e}")
            raise
    
rag_service = RAGService()