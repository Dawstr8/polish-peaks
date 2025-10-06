from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import peaks, photos
from app.database import create_db_and_tables

app = FastAPI(
    title="Polish Peaks API",
    description="API for managing Polish mountain summit photos and achievements",
    version="1.0.0",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(photos.router, prefix="/api/photos", tags=["photos"])
app.include_router(peaks.router, prefix="/api/peaks", tags=["peaks"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Polish Peaks API",
    }
