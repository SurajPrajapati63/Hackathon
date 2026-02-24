from fastapi import FastAPI
from routers.auth_router import router as auth_router

app = FastAPI(title="Auth API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API Running 🚀"}