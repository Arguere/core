from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os 


class Settings(BaseSettings):
    CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")
    CLERK_ISSUER = os.getenv("CLERK_ISSUER")
