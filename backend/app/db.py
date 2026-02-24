"""
Database connection and initialization
"""
from app.config import DATABASE_URL, DATABASE_NAME

# Global database instance
db_client = None
db = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global db_client, db
    try:
        # Try to use motor if available, otherwise just initialize a placeholder
        try:
            from motor.motor_asyncio import AsyncClient
            db_client = AsyncClient(DATABASE_URL)
            db = db_client[DATABASE_NAME]
            await db_client.admin.command('ping')
            print("✅ Connected to MongoDB")
        except ImportError:
            print("⚠️  Motor not installed, using placeholder database")
            db_client = {}
            db = type('MockDB', (), {'name': DATABASE_NAME})()
        except Exception as e:
            print(f"⚠️  MongoDB connection failed: {str(e)}")
            print("⚠️  Using placeholder database")
            db_client = {}
            db = type('MockDB', (), {'name': DATABASE_NAME})()
    except Exception as e:
        print(f"⚠️  Database initialization warning: {str(e)}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    global db_client
    if db_client and hasattr(db_client, 'close'):
        db_client.close()
        print("✅ Closed MongoDB connection")


def get_database():
    """Get database instance"""
    if db is None:
        raise ValueError("Database not initialized")
    return db
