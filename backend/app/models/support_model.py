# backend/app/models/support_model.py

from datetime import datetime
from bson import ObjectId
from typing import Optional, List

from app.db import get_database


class SupportModel:
    collection_name = "support_cases"

    @staticmethod
    def collection(db=None):
        db = db or get_database()
        return db[SupportModel.collection_name]

    @staticmethod
    async def create_ticket(ticket_data: dict, db=None) -> str:
        db = db or get_database()
        ticket = {
            "user_id": ticket_data.get("user_id"),
            "subject": ticket_data.get("subject"),
            "description": ticket_data.get("description"),
            "category": ticket_data.get("category"),
            "booking_id": ticket_data.get("booking_id"),
            "status": ticket_data.get("status", "open"),
            "admin_response": ticket_data.get("admin_response"),
            "created_at": ticket_data.get("created_at", datetime.utcnow()),
            "updated_at": ticket_data.get("updated_at", datetime.utcnow()),
        }
        result = await SupportModel.collection(db).insert_one(ticket)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_user(user_id: str, db=None) -> List[dict]:
        db = db or get_database()
        cursor = SupportModel.collection(db).find({"user_id": user_id})
        return await cursor.to_list(length=100)

    @staticmethod
    async def get_all(db=None) -> List[dict]:
        db = db or get_database()
        cursor = SupportModel.collection(db).find()
        return await cursor.to_list(length=200)

    @staticmethod
    async def get_by_id(ticket_id: str, db=None) -> Optional[dict]:
        db = db or get_database()
        return await SupportModel.collection(db).find_one({"_id": ObjectId(ticket_id)})

    @staticmethod
    async def update_ticket(ticket_id: str, update_data: dict, db=None):
        db = db or get_database()
        await SupportModel.collection(db).update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": update_data}
        )