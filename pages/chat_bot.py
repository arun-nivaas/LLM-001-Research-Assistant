# import neccessary libraries
import streamlit as st
import logging
from rag_pipeline import PDFQA
from llm_client_rag import get_llm_client_rag 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from const import Constants
from dotenv import load_dotenv
import os
from langsmith import Client
import uuid
from s3_client import s3_client, S3_BUCKET_NAME
from ingestion import DoclingPDFLoader


# Load environment variables from .env file
load_dotenv(dotenv_path=".env", override=True)
LANGSMITH_API_KEY = os.getenv(Constants.LANGSMITH_API_KEY)
LANGSMITH_TRACING = os.getenv(Constants.LANGSMITH_TRACING)
LANGSMITH_ENDPOINT = os.getenv(Constants.LANGSMITH_ENDPOINT)
LANGSMITH_PROJECT = os.getenv(Constants.LANGSMITH_PROJECT)

# LangSmith Client and prompt loading
client = Client(api_key = LANGSMITH_API_KEY)
rag_prompt = client.pull_prompt("research_bot_rag_prompt", include_model=False)


# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session state Initilaization 
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = False

if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi 👋 Please upload the document. I’ll answer questions from it."}
        ]


# Conversational Memory
memory = ConversationBufferMemory(
    memory_key = Constants.CHAT_HISTORY,
    return_messages = True,
    output_key = Constants.ANSWER
)


# App configuration
st.set_page_config(layout= Constants.WIDE)


# Header and Description
st.header(Constants.HEADER_TITLE_CHAT_BOT)
st.markdown("---")
st.write(
    "Upload any research paper and instantly chat with it for clear, precise answers."
    "Discover related resources like YouTube, Semantic Scholar, and Wikipedia—all in one place ⚡ "
    "Turn your PDFs into an interactive learning companion 🚀"
)


# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type = Constants.PDF)

if uploaded_file is not None and st.session_state.processed_file is False:
    if st.session_state.api_key:
        st.toast("File uploaded successfully!")
        try:
            with st.spinner("Extracting the text ...."):
                
                # Generate a unique file ID 
                file_id = str(uuid.uuid4())
                s3_key = f"uploads/{file_id}/{uploaded_file.name}"
                logger.info(f"Processing file with ID: {file_id} and name: {uploaded_file.name}")

                # Upload the file to S3
                logger.info("Uploading file to S3...")
                s3_client.upload_fileobj(uploaded_file,S3_BUCKET_NAME,s3_key)
                logger.info("Upload successful.")
                logger.info(f"File uploaded to S3: uploads/{file_id}/{uploaded_file.name}")

                if S3_BUCKET_NAME is None:
                    raise ValueError("S3_BUCKET_NAME is not set. Please check your environment variables or configuration.")
                extract_text = DoclingPDFLoader(bucket_name=S3_BUCKET_NAME, s3_key=s3_key).load()[0].page_content
                logger.info(f"Text extraction completed.{extract_text[:50]}...")
                    
                pdf_qa  = PDFQA(extract_text)
                st.session_state.vector_store = pdf_qa.vector_store 
                st.session_state.pdf_qa = pdf_qa 
                
                logger.info(f"PDF processing and vector store creation completed {st.session_state.vector_store}.")
                    
                # Mark as processed so this block won't run again
                st.session_state.processed_file = True  

        except Exception as e:
            st.session_state.processed_file = False
            st.error(f"Error processing the PDF: {str(e)}")
    else:
        st.error("API key not found")


# ChatGoogleGenerativeAI and RetrievalQA Initialization
if st.session_state.processed_file and st.session_state.qa_chain is None:
    try:
        retriever = st.session_state.pdf_qa.retriever
        llm = get_llm_client_rag(st.session_state.api_key)  
        st.session_state.llm = llm
        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs= {"prompt": rag_prompt},
            memory = memory,
            verbose = True,
            output_key = Constants.ANSWER
        )
        st.session_state.qa_chain = qa_chain

        logger.info("✅ QA chain initialized.")
    except Exception as e:
        st.error(f"Failed to initialize QA chain: {str(e)}")


# AI chat Functionalities (runs independently)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Please enter your prompt here...")

if user_input and st.session_state.api_key and uploaded_file is not None:
    
    with st.chat_message(Constants.USER):
        st.markdown(user_input)
        st.session_state.messages.append({"role": Constants.USER, "content": user_input})

    if not st.session_state.api_key:
        st.toast("❌ Enter your API key...", icon="⚠️")
    elif not st.session_state.processed_file:
        with st.chat_message(Constants.ASSISTANT):
            st.markdown("📄 Please upload a PDF first.")
        st.session_state.messages.append({"role": Constants.ASSISTANT, "content": "📄 Please upload a PDF first."})
    elif st.session_state.qa_chain is None:
        with st.chat_message(Constants.ASSISTANT):
            st.markdown("⚙️ Initializing RAG... please try again in a moment.")
        st.session_state.messages.append({"role": "assistant", "content": "⚙️ Initializing RAG... please try again in a moment."})
    else:
        # Answer via RAG
        try:
            with st.spinner("Thinking..."):

                result = st.session_state.qa_chain.invoke({"question": user_input})
                answer = result.get("answer") or result.get("result") or str(result)  # LC versions differ

                
            with st.chat_message(Constants.ASSISTANT):
                st.markdown(answer)
            st.session_state.messages.append({"role": Constants.ASSISTANT, "content": answer})

            # Optional: Show sources
            # if "source_documents" in result and result["source_documents"]:
            #     with st.expander("🔎 Sources"):
            #         for i, doc in enumerate(result["source_documents"], start=1):
            #             page_snip = doc.page_content[:350].replace("\n", " ")
            #             st.markdown(f"**{i}.** {page_snip}…")

        except Exception as e:
            st.error(f"Error during response generation: {str(e)}")
