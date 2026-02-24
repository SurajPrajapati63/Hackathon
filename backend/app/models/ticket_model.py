# backend/app/models/ticket_model.py

from datetime import datetime
from bson import ObjectId
from typing import Optional

from app.db import get_database


class TicketModel:
    collection_name = "tickets"

    @staticmethod
    def collection(db=None):
        db = db or get_database()
        return db[TicketModel.collection_name]

    @staticmethod
    async def create_ticket(ticket_data: dict, db=None) -> str:
        db = db or get_database()
        ticket = {
            "ticket_code": ticket_data.get("ticket_code"),
            "booking_id": ticket_data.get("booking_id"),
            "user_id": ticket_data.get("user_id"),
            "event_id": ticket_data.get("event_id"),
            "seat_number": ticket_data.get("seat_number"),
            "status": ticket_data.get("status", "active"),
            "created_at": ticket_data.get("created_at", datetime.utcnow()),
            "updated_at": ticket_data.get("updated_at", datetime.utcnow()),
        }
        result = await TicketModel.collection(db).insert_one(ticket)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_code(code: str, db=None) -> Optional[dict]:
        db = db or get_database()
        return await TicketModel.collection(db).find_one({"ticket_code": code})

    @staticmethod
    async def update_status(ticket_id: str, status: str, db=None):
        db = db or get_database()
        _id = ticket_id if isinstance(ticket_id, ObjectId) else ObjectId(ticket_id)
        await TicketModel.collection(db).update_one({"_id": _id}, {"$set": {"status": status}})
    
    @staticmethod
    async def get_by_booking(booking_id: str, db=None):
        db = db or get_database()
        cursor = TicketModel.collection(db).find({"booking_id": booking_id})
        return await cursor.to_list(length=200)

    @staticmethod
    async def update_ticket(ticket_id: str, updates: dict, db=None):
        db = db or get_database()
        _id = ticket_id if isinstance(ticket_id, ObjectId) else ObjectId(ticket_id)
        await TicketModel.collection(db).update_one({"_id": _id}, {"$set": updates})