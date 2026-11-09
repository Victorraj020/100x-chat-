import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Chatbot"
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Allowed CORS origins
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.netlify.app",
        "https://*.vercel.app",
        "https://*.onrender.com",
    ]
    
    # LLM Settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini") # "gemini", "openai", or "fallback"
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Vector Database Settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "") # PostgreSQL + pgvector (e.g. Supabase)
    VECTOR_DIMENSION: int = 768 # Standard dimension for gemini-embedding-004
    TOP_K_RETRIEVAL: int = 4
    SIMILARITY_THRESHOLD: float = 0.35

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

