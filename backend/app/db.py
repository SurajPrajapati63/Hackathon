# backend/app/database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "event_ticket_db")

client: AsyncIOMotorClient = None
database = None


# 🔹 Connect to MongoDB Atlas
async def connect_to_mongo():
    global client, database
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DB_NAME]

    print("✅ Connected to MongoDB Atlas")

    # Create important indexes
    await create_indexes()


# 🔹 Close connection
async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ MongoDB connection closed")


# 🔹 Dependency (used in routes/services)
def get_database():
    return database


# 🔹 Create indexes for performance & uniqueness
async def create_indexes():
    await database["tickets"].create_index("ticket_code", unique=True)
    await database["seats"].create_index(
        [("event_id", 1), ("seat_number", 1)], unique=True
    )
    await database["support"].create_index("user_id")
    await database["entry_logs"].create_index("ticket_id")