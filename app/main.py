from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import tracks, users, methods, scenarios, submissions, feedbacks
from app.core.config import settings
from app.core.database import engine
from app.core.database import Base

app = FastAPI(
    title="Arguere Backend",
    description="Backend API for Arguere learning platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tracks.router, prefix="/api/v1/tracks", tags=["tracks"])
app.include_router(methods.router, prefix="/api/v1/methods", tags=["methods"])
app.include_router(scenarios.router, prefix="/api/v1/scenarios", tags=["scenarios"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["submissions"])
app.include_router(feedbacks.router, prefix="/api/v1/feedback", tags=["feedback"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}