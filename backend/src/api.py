from fastapi import FastAPI

from src.peaks.controller import router as peaks_router
from src.photos.controller import router as photos_router
from src.users.controller import router as users_router


def register_routes(app: FastAPI):
    app.include_router(users_router)
    app.include_router(peaks_router)
    app.include_router(photos_router)
