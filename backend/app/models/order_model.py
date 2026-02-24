from datetime import datetime
from typing import Optional

from app.db import get_database


class OrderModel:
    collection_name = "orders"

    @staticmethod
    def collection(db=None):
        db = db or get_database()
        return db[OrderModel.collection_name]

    @staticmethod
    async def create_order(order_data: dict, db=None) -> str:
        db = db or get_database()
        from bson import ObjectId

        order = {
            "user_id": ObjectId(order_data.get("user_id")),
            "event_id": ObjectId(order_data.get("event_id")),
            "total_amount": order_data.get("total_amount"),
            "payment_mode": order_data.get("payment_mode"),
            "order_status": order_data.get("order_status", "pending"),
            "booking_time": datetime.utcnow()
        }
        result = await OrderModel.collection(db).insert_one(order)
        return str(result.inserted_id)

    @staticmethod
    async def update_status(order_id: str, status: str, db=None):
        db = db or get_database()
        from bson import ObjectId

        _id = order_id if isinstance(order_id, ObjectId) else ObjectId(order_id)
        await OrderModel.collection(db).update_one({"_id": _id}, {"$set": {"order_status": status}})