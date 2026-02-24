# backend/app/models/event_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class EventModel:
    collection_name = "events"

    @staticmethod
    def collection(db):
        return db[EventModel.collection_name]

    @staticmethod
    async def create_event(db, name, category, event_date, ticket_price,
                           max_tickets_per_user, venue_id, organizer_id):
        event = {
            "name": name,
            "category": category,
            "event_date": event_date,
            "ticket_price": ticket_price,
            "max_tickets_per_user": max_tickets_per_user,
            "venue_id": ObjectId(venue_id),
            "organizer_id": ObjectId(organizer_id),
            "status": "upcoming",  # upcoming | closed | cancelled
            "created_at": datetime.utcnow()
        }
        result = await EventModel.collection(db).insert_one(event)
        event["_id"] = result.inserted_id
        return event

    @staticmethod
    async def get_by_id(db, event_id):
        return await EventModel.collection(db).find_one({"_id": ObjectId(event_id)})

    @staticmethod
    async def list_upcoming(db):
        cursor = EventModel.collection(db).find({"status": "upcoming"})
        return await cursor.to_list(None)