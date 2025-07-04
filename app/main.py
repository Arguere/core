from fastapi import FastAPI
from app.routes.audio import router as audio_router

app = FastAPI(title="Arguere", version="0.1.0")

app.include_router(audio_router, prefix="/audio", tags=["audio"])