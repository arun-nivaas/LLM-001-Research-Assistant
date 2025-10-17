from fastapi import Request
from fastapi.responses import JSONResponse
from handlers.exceptions import ChunkingError, EmbeddingError, RetrieverError

async def chunking_error_handler(request: Request, exc: ChunkingError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"status": "error", "type": "ChunkingError", "message": str(exc)},
    )

async def embedding_error_handler(request: Request, exc: EmbeddingError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"status": "error", "type": "EmbeddingError", "message": str(exc)},
    )

async def retriever_error_handler(request: Request, exc: RetrieverError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"status": "error", "type": "RetrieverError", "message": str(exc)},
    )

# Catch-all fallback
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "type": "InternalServerError", "message": str(exc)},
    )
