# backend/app/models/refund_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class RefundModel:
    collection_name = "refunds"

    @staticmethod
    def collection(db):
        return db[RefundModel.collection_name]

    @staticmethod
    async def create_refund(db, order_id, ticket_id, user_id, event_id, reason):
        refund = {
            "order_id": ObjectId(order_id),
            "ticket_id": ObjectId(ticket_id),
            "user_id": ObjectId(user_id),
            "event_id": ObjectId(event_id),
            "reason": reason,
            "status": "pending",  # pending | approved | rejected
            "created_at": datetime.utcnow()
        }
        result = await RefundModel.collection(db).insert_one(refund)
        refund["_id"] = result.inserted_id
        return refund

    @staticmethod
    async def update_status(db, refund_id, status):
        await RefundModel.collection(db).update_one(
            {"_id": ObjectId(refund_id)},
            {"$set": {"status": status}}
        )