# Import necessary libraries
import pdfplumber
import logging
import streamlit as st
from io import BytesIO
from s3_client import s3_client
from PyPDF2 import PdfReader


logger = logging.getLogger(__name__)

# Function to extract text from PDF file formats

@st.cache_data(show_spinner=False)
def extract_text_from_pdf(bucket_name: str, s3_key: str) -> str:
    text_parts = []

    pdf_obj = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
    logger.info("Downloading file from S3 for processing...")
    pdf_bytes = pdf_obj['Body'].read()
    logger.info("Download successful.")

    # Step 1: Use LangChain’s PyPDFLoader
    reader = PdfReader(BytesIO(pdf_bytes))
    for page in reader.pages:
        text = page.extract_text()

        if text:
            text_parts.append(text)

    # Step 2: Fallback → extract tables with pdfplumber
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                table_text = "\n".join(
                    [", ".join(str(cell) if cell else "" for cell in row) for row in table if row]
                )
                if table_text.strip():
                    text_parts.append(table_text)

    return "\n".join(text_parts)


# # # Function to extract text from DOCX file formats
# # import docx

# # # Function to extract text from DOCX file formats (handles paragraphs + tables)
# # def extract_text_from_docx(path):
# #     if not os.path.exists(path):
# #         raise FileNotFoundError(f"File not found: {path}")
    
# #     doc = docx.Document(path)
# #     text_parts = []

# #     # Extract all paragraphs
# #     for p in doc.paragraphs:
# #         if p.text.strip():
# #             text_parts.append(p.text.strip())

# #     # Extract text from tables
# #     for table in doc.tables:
# #         for row in table.rows:
# #             row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
# #             if row_text:
# #                 text_parts.append(" | ".join(row_text))  # join cells with a separator

# #     return clean_text("\n".join(text_parts))


# # Function to extract text from TXT file formats
# def extract_text_from_txt(path):
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"File not found: {path}")
    
#     loader = TextLoader(path, encoding="utf-8")
#     docs = loader.load()
#     return clean_text("\n".join([d.page_content for d in docs]))


# # Function to extract text from various file formats
# # Supports PDF, DOCX, and TXT formats
# def extract_text(path):
#     path = os.path.abspath(path)
#     if path.lower().endswith(".pdf"):
#         return extract_text_from_pdf(path)
#     elif path.lower().endswith(".docx"):
#         return extract_text_from_docx(path)
#     elif path.lower().endswith(".txt"):
#         return extract_text_from_txt(path)
#     else:
#         raise ValueError("Unsupported format: PDF/DOCX/TXT supported.")
    


# resume_folder = "resume_data/resumes/"
# all_resumes_text = []
# resume_txt = []

# for file_name in os.listdir(resume_folder):
#     file_path = os.path.join(resume_folder, file_name)
#     try:
#         text = extract_text(file_path)  # LangChain-powered extractor
#         resume_txt.append(text)
#         all_resumes_text.append({"file": file_name, "content": text})
#     except Exception as e:
#         print(f"Error processing {file_name}: {e}")

# # Save all resume contents to a JSON file
# with open("resumes.json", "w", encoding="utf-8") as f:
#     json.dump(all_resumes_text, f, indent=4, ensure_ascii=False)



