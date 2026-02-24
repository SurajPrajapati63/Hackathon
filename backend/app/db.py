from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Shared client/database references
client: AsyncIOMotorClient | None = None
database = None
db = None  # backward-compatible alias


async def connect_to_mongo():
    """Initialize the MongoDB client and database (called on startup)."""
    global client, database, db
    client = AsyncIOMotorClient(settings.MONGO_URL)
    database = client[settings.DATABASE_NAME]
    db = database
    await create_indexes()


async def close_mongo_connection():
    global client
    if client:
        client.close()


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