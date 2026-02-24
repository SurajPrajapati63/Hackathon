# backend/app/models/event_model.py

from datetime import datetime
from bson import ObjectId
from typing import Optional, List

from app.db import get_database


class EventModel:
    collection_name = "events"

    @staticmethod
    def collection(db=None):
        db = db or get_database()
        return db[EventModel.collection_name]

    @staticmethod
    async def create_event(event_data: dict, db=None) -> str:
        db = db or get_database()
        doc = {
            "title": event_data.get("title") or event_data.get("name"),
            "description": event_data.get("description"),
            "category": event_data.get("category"),
            "event_date": event_data.get("event_date"),
            "ticket_price": event_data.get("ticket_price", 0),
            "total_seats": event_data.get("total_seats", 0),
            "tickets_sold": event_data.get("tickets_sold", 0),
            "venue_id": event_data.get("venue_id"),
            "organizer_id": event_data.get("organizer_id"),
            "status": event_data.get("status", "upcoming"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await EventModel.collection(db).insert_one(doc)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(event_id: str, db=None) -> Optional[dict]:
        db = db or get_database()
        return await EventModel.collection(db).find_one({"_id": ObjectId(event_id)})

    @staticmethod
    async def get_all(db=None) -> List[dict]:
        db = db or get_database()
        cursor = EventModel.collection(db).find()
        return await cursor.to_list(length=200)

    @staticmethod
    async def get_by_organizer(organizer_id: str, db=None) -> List[dict]:
        db = db or get_database()
        cursor = EventModel.collection(db).find({"organizer_id": organizer_id})
        return await cursor.to_list(length=200)

    @staticmethod
    async def update_event(event_id: str, updates: dict, db=None):
        db = db or get_database()
        _id = event_id if isinstance(event_id, ObjectId) else ObjectId(event_id)
        await EventModel.collection(db).update_one({"_id": _id}, {"$set": updates})

    @staticmethod
    async def delete_event(event_id: str, db=None):
        db = db or get_database()
        await EventModel.collection(db).delete_one({"_id": ObjectId(event_id)})
