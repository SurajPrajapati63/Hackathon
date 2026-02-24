from fastapi import FastAPI
from routers.auth_router import router as auth_router
from app.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Auth API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API Running 🚀"}

# backend/app/main.py



app = FastAPI()


@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()