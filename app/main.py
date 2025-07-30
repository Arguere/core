from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.endpoints import feedback, scenario, submission
from app.core.database import  init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Initialize the database
    await init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Monolog Core",
    description="Backend API for Monolog learning platform",
    version="1.0.0"
)


app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])
app.include_router(scenario.router, prefix="/api/scenario", tags=["scenario"])
app.include_router(submission.router, prefix="/api/submission", tags=["submission"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}