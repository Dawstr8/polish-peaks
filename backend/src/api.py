from fastapi import FastAPI

from src.auth.controller import router as auth_router
from src.peaks.controller import router as peaks_router
from src.photos.controller import router as photos_router


def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(peaks_router)
    app.include_router(photos_router)
