# backend/app/main.py

from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.routes import (
    auth_routes,
    admin_router,
    organizer_router,
    customer_router,
    support_router,
    entry_router
)
from app.db import client


# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="Event Ticket Booking API",
    description="Production-ready Event Ticket Booking Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# -----------------------------
# Add Middlewares
# -----------------------------
add_cors_middleware(app)
app.add_middleware(LoggingMiddleware)


# -----------------------------
# Database Startup Check
# -----------------------------
@app.on_event("startup")
async def startup_db():
    try:
        await client.admin.command("ping")
        print("✅ MongoDB Connected Successfully!")
    except Exception as e:
        print("❌ MongoDB Connection Failed!")
        print(str(e))


# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/health")
async def health_check():
    return {"status": "Server is running 🚀"}


# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_routes.router)
app.include_router(admin_router.router)
app.include_router(organizer_router.router)
app.include_router(customer_router.router)
app.include_router(support_router.router)
app.include_router(entry_router.router)