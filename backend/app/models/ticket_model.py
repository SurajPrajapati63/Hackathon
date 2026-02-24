# backend/app/models/ticket_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid


class TicketModel:
    collection_name = "tickets"

    @staticmethod
    def collection(db):
        return db[TicketModel.collection_name]

    @staticmethod
    async def create_ticket(db, order_id, user_id, event_id, seat_id):
        ticket = {
            "ticket_code": str(uuid.uuid4()),
            "order_id": ObjectId(order_id),
            "user_id": ObjectId(user_id),
            "event_id": ObjectId(event_id),
            "seat_id": ObjectId(seat_id),
            "status": "valid",  # valid | used | cancelled
            "created_at": datetime.utcnow()
        }
        result = await TicketModel.collection(db).insert_one(ticket)
        ticket["_id"] = result.inserted_id
        return ticket

    @staticmethod
    async def get_by_code(db, code):
        return await TicketModel.collection(db).find_one({"ticket_code": code})

    @staticmethod
    async def update_status(db, ticket_id, status):
        await TicketModel.collection(db).update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": {"status": status}}
        )