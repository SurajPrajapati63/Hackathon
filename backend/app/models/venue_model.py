# backend/app/models/venue_model.py

from datetime import datetime
from typing import Optional, List

from app.db import get_database


class VenueModel:
    collection_name = "venues"

    @staticmethod
    def collection(db=None):
        db = db if db is not None else get_database()
        return db[VenueModel.collection_name]

    @staticmethod
    async def create_venue(venue_data: dict, db=None) -> str:
        db = db if db is not None else get_database()
        now = datetime.utcnow()
        venue = {
            "name": venue_data.get("name"),
            "location": venue_data.get("location"),
            "capacity": venue_data.get("capacity"),
            "description": venue_data.get("description"),
            "created_at": now,
            "updated_at": now,
        }
        result = await VenueModel.collection(db).insert_one(venue)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(venue_id: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        from bson import ObjectId

        return await VenueModel.collection(db).find_one({"_id": ObjectId(venue_id)})

    @staticmethod
    async def get_all(db=None) -> List[dict]:
        db = db if db is not None else get_database()
        cursor = VenueModel.collection(db).find()
        return await cursor.to_list(length=200)

    @staticmethod
    async def update_venue(venue_id: str, updates: dict, db=None):
        db = db if db is not None else get_database()
        from bson import ObjectId

        _id = venue_id if isinstance(venue_id, ObjectId) else ObjectId(venue_id)
        updates["updated_at"] = datetime.utcnow()
        await VenueModel.collection(db).update_one({"_id": _id}, {"$set": updates})

    @staticmethod
    async def delete_venue(venue_id: str, db=None):
        db = db if db is not None else get_database()
        from bson import ObjectId

        await VenueModel.collection(db).delete_one({"_id": ObjectId(venue_id)})