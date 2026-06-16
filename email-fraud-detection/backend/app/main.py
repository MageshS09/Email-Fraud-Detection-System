from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import create_app
from app.core.config import settings

app: FastAPI = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
