from fastapi import APIRouter, HTTPException
from models import ProcessPDFRequest
from services.ingestion import DoclingPDFLoader
from services.rag_service import rag_service
from config import settings
from handlers.exceptions import ChunkingError, EmbeddingError
import logging

# Initialize logger
logger = logging.getLogger("pdf_router")
logger.setLevel(logging.INFO)

# Create a router for PDF-related endpoints
router = APIRouter(tags=["PDF"])

@router.post("/process_pdf")
async def process_pdf(request: ProcessPDFRequest):
    """
    Endpoint to process a PDF from S3 and store it in RAG service.
    """
    if not request.s3_key.strip():
        raise HTTPException(status_code=400, detail="s3_key cannot be empty")

    try:
        logger.info(f"Processing PDF from S3 key: {request.s3_key}")

        # Load PDF content
        try:
            extract_text = DoclingPDFLoader(
                bucket_name=settings.S3_BUCKET_NAME,
                s3_key=request.s3_key
            ).load()[0].page_content
        except Exception as e:
            raise ChunkingError(f"PDF chunking failed: {e}")

        # Process PDF using RAG service
        try:
            rag_service.process_pdf(extract_text, request.api_key)
        except Exception as e:
            raise EmbeddingError(f"RAG processing failed: {e}")

        return {"status": "success", "message": "PDF processed successfully."}

    except (ChunkingError, EmbeddingError) as e:
        # These will be caught by your FastAPI exception handlers
        raise e
    except Exception as e:
        # Generic fallback
        raise HTTPException(status_code=500, detail=f"Error processing the PDF: {str(e)}")
