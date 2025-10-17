from fastapi import FastAPI,HTTPException
from models import QueryRequest, QueryResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from services.rag_service import rag_service
from handlers.handlers import (
    chunking_error_handler,
    embedding_error_handler,
    retriever_error_handler,
    global_exception_handler,
)
from routers import router as process_pdf_router
from routers.evaluation_router import router as evaluation_router
from handlers.exceptions import ChunkingError, EmbeddingError, RetrieverError

app = FastAPI(title = "Research Assistant Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ChunkingError, chunking_error_handler) #type: ignore
app.add_exception_handler(EmbeddingError, embedding_error_handler) #type: ignore
app.add_exception_handler(RetrieverError, retriever_error_handler) #type: ignore
app.add_exception_handler(Exception, global_exception_handler)


app.include_router(process_pdf_router)

@app.post("/query", response_model = QueryResponse)
async def query_manual(request:QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code = 400, detail="Query cannot be empty")
    
    try:
        answer, source = rag_service.query(request.query)
        return QueryResponse(answer = answer, context=" ".join(source) if source else "")     
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Error processing the PDF: {str(e)}")


app.include_router(evaluation_router, prefix="/evaluate", tags=["Evaluation"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)   