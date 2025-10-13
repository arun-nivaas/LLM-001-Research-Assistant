from fastapi import FastAPI,HTTPException
from models import QueryRequest, QueryResponse, ProcessPDFRequest
from ingestion import DoclingPDFLoader
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from rag_service import rag_service
from config import settings


app = FastAPI(title = "Research Assistant Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process_pdf")
async def process_pdf(request: ProcessPDFRequest):
    try:
        # Process PDF using Docling loader
        extract_text = DoclingPDFLoader(
            bucket_name = settings.S3_BUCKET_NAME,
            s3_key = request.s3_key
        ).load()[0].page_content

        rag_service.process_pdf(extract_text, request.api_key)
        return {"message": "PDF processed successfully."}

    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Error processing the PDF: {str(e)}")


@app.post("/query", response_model = QueryResponse)
async def query_manual(request:QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code = 400, detail="Query cannot be empty")
    
    try:
        answer, source = rag_service.query(request.query)
        return QueryResponse(answer = answer, context=" ".join(source) if source else "")     
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Error processing the PDF: {str(e)}")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)   