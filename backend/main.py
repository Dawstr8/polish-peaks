from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import register_routes
from src.database.core import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully")
    yield
    pass


app = FastAPI(
    title="Polish Peaks API",
    description="API for managing Polish mountain summit photos and achievements",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

register_routes(app)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Polish Peaks API",
    }
