# backend/app/models/seat_model.py

from datetime import datetime
from bson import ObjectId
from typing import List, Optional

from app.db import get_database


class SeatModel:
    collection_name = "seats"

    @staticmethod
    def collection(db=None):
        db = db if db is not None else get_database()
        return db[SeatModel.collection_name]

    @staticmethod
    async def create_seat(event_id: str, seat_number: str, db=None) -> str:
        db = db if db is not None else get_database()
        seat = {
            "event_id": event_id,
            "seat_number": seat_number,
            "status": "available",
            "locked_by": None,
            "lock_expiry": None,
            "created_at": datetime.utcnow(),
        }
        result = await SeatModel.collection(db).insert_one(seat)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_event(event_id: str, db=None) -> List[dict]:
        db = db if db is not None else get_database()
        cursor = SeatModel.collection(db).find({"event_id": event_id})
        return await cursor.to_list(length=500)

    @staticmethod
    async def get_by_event_and_seat(event_id: str, seat_number: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        return await SeatModel.collection(db).find_one({"event_id": event_id, "seat_number": seat_number})

    @staticmethod
    async def update_seat(seat_id: str, updates: dict, db=None):
        db = db if db is not None else get_database()
        _id = seat_id if isinstance(seat_id, ObjectId) else ObjectId(seat_id)
        await SeatModel.collection(db).update_one({"_id": _id}, {"$set": updates})

    @staticmethod
    async def get_expired_locks(now, db=None) -> List[dict]:
        db = db if db is not None else get_database()
        cursor = SeatModel.collection(db).find({"status": "locked", "lock_expiry": {"$lte": now}})
        return await cursor.to_list(length=500)