# backend/app/models/seat_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class SeatModel:
    collection_name = "seats"

    @staticmethod
    def collection(db):
        return db[SeatModel.collection_name]

    @staticmethod
    async def create_seat(db, event_id, seat_number):
        seat = {
            "event_id": ObjectId(event_id),
            "seat_number": seat_number,
            "status": "available",  # available | booked
            "created_at": datetime.utcnow()
        }
        result = await SeatModel.collection(db).insert_one(seat)
        seat["_id"] = result.inserted_id
        return seat

    @staticmethod
    async def get_available_seats(db, event_id):
        cursor = SeatModel.collection(db).find({
            "event_id": ObjectId(event_id),
            "status": "available"
        })
        return await cursor.to_list(None)

    @staticmethod
    async def update_status(db, seat_id, status):
        await SeatModel.collection(db).update_one(
            {"_id": ObjectId(seat_id)},
            {"$set": {"status": status}}
        )