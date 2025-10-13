from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LangSmith Configuration
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: str = ""
    LANGSMITH_ENDPOINT: str = ""
    langsmith_project: str = ""
    
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""
    S3_BUCKET_NAME: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create a global settings instance
settings = Settings()