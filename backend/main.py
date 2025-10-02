from datetime import datetime

from fastapi import FastAPI

app = FastAPI(
    title="Polish Peaks API",
    description="API for managing Polish mountain summit photos and achievements",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Polish Peaks API",
    }
