# backend/app/models/venue_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class VenueModel:
    collection_name = "venues"

    @staticmethod
    def collection(db):
        return db[VenueModel.collection_name]

    @staticmethod
    async def create_venue(db, name, city, total_capacity, address):
        venue = {
            "name": name,
            "city": city,
            "total_capacity": total_capacity,
            "address": address,
            "created_at": datetime.utcnow()
        }
        result = await VenueModel.collection(db).insert_one(venue)
        venue["_id"] = result.inserted_id
        return venue

    @staticmethod
    async def get_by_id(db, venue_id):
        return await VenueModel.collection(db).find_one({"_id": ObjectId(venue_id)})