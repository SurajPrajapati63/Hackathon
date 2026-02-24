# backend/app/main.py

from fastapi import FastAPI

from app.middleware.cors import add_cors_middleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.db import connect_to_mongo, close_mongo_connection
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.organizer_router import router as organizer_router
from app.routers.customer_router import router as customer_router
from app.routers.support_router import router as support_router
from app.routers.entry_router import router as entry_router


app = FastAPI(
    title="Event Ticket Booking API",
    description="Production-ready Event Ticket Booking Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


add_cors_middleware(app)
app.add_middleware(LoggingMiddleware)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(organizer_router)
app.include_router(customer_router)
app.include_router(support_router)
app.include_router(entry_router)


@app.on_event("startup")
async def startup():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


@app.get("/health")
async def health_check():
    return {"status": "Server is running 🚀"}
