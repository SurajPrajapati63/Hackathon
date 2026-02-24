from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    logger.info("🔄 Connecting to MongoDB...")

    client = AsyncIOMotorClient(settings.MONGO_URL)
    database = client[settings.DATABASE_NAME]

    logger.info("✅ MongoDB Connected Successfully!")

except Exception as e:
    logger.error("❌ MongoDB Connection Failed!")
    logger.error(str(e))


def get_db():
    return database