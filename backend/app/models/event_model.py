# backend/app/models/event_model.py

from datetime import datetime
from bson import ObjectId
from app.database import db


class EventModel:
    collection = db["events"]

    @staticmethod
    async def create_event(event_data: dict):
        event_data["tickets_sold"] = 0
        event_data["status"] = "upcoming"  # upcoming | ongoing | completed | cancelled
        event_data["created_at"] = datetime.utcnow()
        event_data["updated_at"] = datetime.utcnow()

        result = await EventModel.collection.insert_one(event_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(event_id: str):
        return await EventModel.collection.find_one({"_id": ObjectId(event_id)})

    @staticmethod
    async def get_by_organizer(organizer_id: str):
        return await EventModel.collection.find(
            {"organizer_id": organizer_id}
        ).to_list(length=100)

    @staticmethod
    async def get_all():
        return await EventModel.collection.find().to_list(length=100)

    @staticmethod
    async def update_event(event_id: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow()
        return await EventModel.collection.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )

    @staticmethod
    async def delete_event(event_id: str):
        return await EventModel.collection.delete_one({"_id": ObjectId(event_id)})