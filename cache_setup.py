import os
from pathlib import Path
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache

def init_cache(db_path: str | None = None):
    """
    Initialize a persistent SQLite cache for LangChain.

    Parameters
    ----------
    db_path : str | None
        Path to the SQLite database file. Defaults to a 'cache' folder.
    """
    if db_path is None:
        # Store in a dedicated folder for easy backups & versioning
        cache_dir = Path("cache")
        cache_dir.mkdir(exist_ok=True)
        db_path = cache_dir / "langchain_cache.sqlite"

    # Register cache globally
    set_llm_cache(SQLiteCache(database_path=str(db_path)))
    return db_path