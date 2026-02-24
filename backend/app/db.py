from motor.motor_asyncio import AsyncIOMotorClient
from backend.app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
database = client[settings.DATABASE_NAME]


def get_db():
    return database