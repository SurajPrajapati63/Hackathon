from app.config import settings
from typing import Any

# Delay importing motor until we actually connect to avoid import-time errors

# Shared client/database references
client: Any = None
database = None
db = None  # backward-compatible alias


async def connect_to_mongo():
    """Initialize the MongoDB client and database (called on startup)."""
    global client, database, db
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        client = AsyncIOMotorClient(settings.MONGO_URL)
        database = client[settings.DATABASE_NAME]
        db = database

        await create_indexes()
        print("✅ Connected to MongoDB")
    except Exception as e:
        # Could be ImportError (motor/pymongo/bson mismatch) or connection error
        print("⚠️ Could not connect to MongoDB:", str(e))
        client = None
        database = None
        db = None


async def close_mongo_connection():
    global client
    if client:
        try:
            client.close()
        except Exception:
            pass


def get_database():
    return database


async def create_indexes():
    if database is None:
        return
    await database["tickets"].create_index("ticket_code", unique=True)
    await database["seats"].create_index(
        [("event_id", 1), ("seat_number", 1)], unique=True
    )
    await database["support"].create_index("user_id")
    await database["entry_logs"].create_index("ticket_id")