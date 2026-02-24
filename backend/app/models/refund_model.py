# backend/app/models/refund_model.py

from datetime import datetime
from bson import ObjectId
from typing import Optional, List

from app.db import get_database


class RefundModel:
    collection_name = "refunds"

    @staticmethod
    def collection(db=None):
        db = db if db is not None else get_database()
        return db[RefundModel.collection_name]

    @staticmethod
    async def create_refund(refund_data: dict, db=None) -> str:
        db = db if db is not None else get_database()
        doc = {
            "booking_id": refund_data.get("booking_id"),
            "user_id": refund_data.get("user_id"),
            "refund_amount": refund_data.get("refund_amount"),
            "reason": refund_data.get("reason"),
            "status": refund_data.get("status", "requested"),
            "created_at": refund_data.get("created_at", datetime.utcnow()),
            "updated_at": refund_data.get("updated_at", datetime.utcnow()),
        }
        result = await RefundModel.collection(db).insert_one(doc)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_booking(booking_id: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        return await RefundModel.collection(db).find_one({"booking_id": booking_id})

    @staticmethod
    async def get_by_id(refund_id: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        return await RefundModel.collection(db).find_one({"_id": ObjectId(refund_id)})

    @staticmethod
    async def update_refund(refund_id: str, updates: dict, db=None):
        db = db if db is not None else get_database()
        _id = refund_id if isinstance(refund_id, ObjectId) else ObjectId(refund_id)
        await RefundModel.collection(db).update_one({"_id": _id}, {"$set": updates})