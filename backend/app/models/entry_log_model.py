# backend/app/models/entry_log_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class EntryLogModel:
    collection_name = "entry_logs"

    @staticmethod
    def collection(db):
        return db[EntryLogModel.collection_name]

    @staticmethod
    async def log_entry(db, ticket_id, entry_manager_id):
        log = {
            "ticket_id": ObjectId(ticket_id),
            "entry_manager_id": ObjectId(entry_manager_id),
            "entry_time": datetime.utcnow()
        }
        result = await EntryLogModel.collection(db).insert_one(log)
        log["_id"] = result.inserted_id
        return log