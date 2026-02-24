# backend/app/models/order_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class OrderModel:
    collection_name = "orders"

    @staticmethod
    def collection(db):
        return db[OrderModel.collection_name]

    @staticmethod
    async def create_order(db, user_id, event_id, total_amount, payment_mode):
        order = {
            "user_id": ObjectId(user_id),
            "event_id": ObjectId(event_id),
            "total_amount": total_amount,
            "payment_mode": payment_mode,
            "order_status": "pending",  # pending | confirmed | cancelled | refunded
            "booking_time": datetime.utcnow()
        }
        result = await OrderModel.collection(db).insert_one(order)
        order["_id"] = result.inserted_id
        return order

    @staticmethod
    async def update_status(db, order_id, status):
        await OrderModel.collection(db).update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"order_status": status}}
        )