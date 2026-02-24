# backend/app/middleware/cors.py

from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",   # React
            "http://127.0.0.1:3000",
            "http://localhost:8501",   # Streamlit
            "http://127.0.0.1:8501",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )