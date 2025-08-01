from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os 

load_dotenv()

class Settings(BaseSettings):
    CLERK_JWKS_URL: str = os.getenv("CLERK_JWKS_URL")
    CLERK_ISSUER: str = os.getenv("CLERK_ISSUER")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ASSEMBLYAI_API_KEY: str = os.getenv("ASSEMBLYAI_API_KEY")
    ENV: str = os.getenv("ENV", "development")

    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()