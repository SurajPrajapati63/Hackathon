"""
Configuration settings for the FastAPI application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = "event_booking_db"

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8501",
    "http://localhost:8000",
]

# Application Settings
APP_NAME = "Event Ticket Booking API"
APP_VERSION = "1.0.0"

# Logging
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
