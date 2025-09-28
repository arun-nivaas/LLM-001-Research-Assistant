from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@traceable
def get_llm_client_rag(api_key:str):

    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        google_api_key = api_key,
        safety_settings = {
    0: 2,  # DANGEROUS_CONTENT → medium block
    1: 2,  # HARASSMENT → medium block
    2: 2,  # HATE_SPEECH → medium block
    3: 2   # SEXUALLY_EXPLICIT → medium block
    },
    temperature = 0.5)
        
    return llm
    