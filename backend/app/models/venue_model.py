# backend/app/models/venue_model.py

from datetime import datetime
from typing import Optional

from app.db import get_database


class VenueModel:
    collection_name = "venues"

    @staticmethod
    def collection(db=None):
        db = db or get_database()
        return db[VenueModel.collection_name]

    @staticmethod
    async def create_venue(venue_data: dict, db=None) -> str:
        db = db or get_database()
        venue = {
            "name": venue_data.get("name"),
            "city": venue_data.get("city"),
            "total_capacity": venue_data.get("total_capacity"),
            "address": venue_data.get("address"),
            "created_at": datetime.utcnow()
        }
        result = await VenueModel.collection(db).insert_one(venue)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(venue_id: str, db=None) -> Optional[dict]:
        db = db or get_database()
        from bson import ObjectId

        return await VenueModel.collection(db).find_one({"_id": ObjectId(venue_id)})