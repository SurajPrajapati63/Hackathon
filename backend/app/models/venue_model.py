# backend/app/models/venue_model.py

from datetime import datetime
from bson import ObjectId
from app.database import db


class VenueModel:
    collection = db["venues"]

    @staticmethod
    async def create_venue(venue_data: dict):
        venue_data["created_at"] = datetime.utcnow()
        venue_data["updated_at"] = datetime.utcnow()

        result = await VenueModel.collection.insert_one(venue_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(venue_id: str):
        return await VenueModel.collection.find_one({"_id": ObjectId(venue_id)})

    @staticmethod
    async def get_all():
        return await VenueModel.collection.find().to_list(length=100)

    @staticmethod
    async def update_venue(venue_id: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow()
        return await VenueModel.collection.update_one(
            {"_id": ObjectId(venue_id)},
            {"$set": update_data}
        )

    @staticmethod
    async def delete_venue(venue_id: str):
        return await VenueModel.collection.delete_one({"_id": ObjectId(venue_id)})