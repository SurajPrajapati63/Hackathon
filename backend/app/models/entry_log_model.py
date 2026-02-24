from datetime import datetime
from bson import ObjectId
from typing import List, Optional

from app.db import get_database


class EntryLogModel:
    collection_name = "entry_logs"

    @staticmethod
    def collection(db=None):
        db = db if db is not None else get_database()
        return db[EntryLogModel.collection_name]

    @staticmethod
    async def create_entry(entry_data: dict, db=None) -> str:
        db = db if db is not None else get_database()
        doc = {
            "ticket_id": entry_data.get("ticket_id"),
            "event_id": entry_data.get("event_id"),
            "validated_by": entry_data.get("validated_by"),
            "device_info": entry_data.get("device_info"),
            "entry_time": entry_data.get("entry_time", datetime.utcnow()),
        }
        result = await EntryLogModel.collection(db).insert_one(doc)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_event(event_id: str, db=None) -> List[dict]:
        db = db if db is not None else get_database()
        cursor = EntryLogModel.collection(db).find({"event_id": event_id})
        return await cursor.to_list(length=500)

    @staticmethod
    async def get_by_ticket(ticket_id: str, db=None) -> List[dict]:
        db = db if db is not None else get_database()
        cursor = EntryLogModel.collection(db).find({"ticket_id": ticket_id})
        return await cursor.to_list(length=200)
