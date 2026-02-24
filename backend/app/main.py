from fastapi import FastAPI
from app.routers import auth_router
from app.db import client

app = FastAPI(
    title="Event Ticket Booking API",
    version="1.0.0"
)


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
# Include Routers
# -----------------------------
app.include_router(auth_routes.router)