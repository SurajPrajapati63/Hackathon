"""
CORS Middleware
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS


def add_cors_middleware(app: FastAPI):
    """Add CORS middleware to the application"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
