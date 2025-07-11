from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Arguere Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/arguere")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://arguere.com"]
    AUDIO_UPLOAD_DIR: str = "./uploads/audio"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "your-llm-api-key")
    ASSEMBLY_AI_API_KEY: str = os.getenv("ASSEMBLY_AI_API_KEY", "your-assemblyai-api-key")
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY", "your-cerebras-api-key")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()