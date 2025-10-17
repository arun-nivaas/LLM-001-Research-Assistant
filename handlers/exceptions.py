class ChunkingError(Exception):
    """Raised when text chunking fails."""
    pass

class EmbeddingError(Exception):
    """Raised when embedding creation fails."""
    pass

class RetrieverError(Exception):
    """Raised when retriever setup fails."""
    pass