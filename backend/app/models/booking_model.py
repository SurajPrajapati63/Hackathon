from datetime import datetime
from bson import ObjectId
from typing import Optional, List

from app.db import get_database


class BookingModel:
	collection_name = "bookings"

	@staticmethod
	def collection(db=None):
		db = db if db is not None else get_database()
		return db[BookingModel.collection_name]

	@staticmethod
	async def create_booking(booking_data: dict, db=None) -> str:
		db = db if db is not None else get_database()
		doc = {
			"user_id": booking_data.get("user_id"),
			"event_id": booking_data.get("event_id"),
			"seat_numbers": booking_data.get("seat_numbers", []),
			"total_amount": booking_data.get("total_amount", 0),
			"booking_status": booking_data.get("booking_status", "pending"),
			"payment_status": booking_data.get("payment_status", "unpaid"),
			"created_at": booking_data.get("created_at", datetime.utcnow()),
			"updated_at": booking_data.get("updated_at", datetime.utcnow()),
		}
		result = await BookingModel.collection(db).insert_one(doc)
		return str(result.inserted_id)

	@staticmethod
	async def get_by_id(booking_id: str, db=None) -> Optional[dict]:
		db = db if db is not None else get_database()
		return await BookingModel.collection(db).find_one({"_id": ObjectId(booking_id)})

	@staticmethod
	async def update_booking(booking_id: str, updates: dict, db=None):
		db = db if db is not None else get_database()
		_id = booking_id if isinstance(booking_id, ObjectId) else ObjectId(booking_id)
		await BookingModel.collection(db).update_one({"_id": _id}, {"$set": updates})

	@staticmethod
	async def list_by_user(user_id: str, db=None) -> List[dict]:
		db = db if db is not None else get_database()
		cursor = BookingModel.collection(db).find({"user_id": user_id})
		return await cursor.to_list(length=100)

	@staticmethod
	async def get_by_user(user_id: str, db=None) -> List[dict]:
		"""Compatibility wrapper used by routers/services expecting `get_by_user`."""
		return await BookingModel.list_by_user(user_id, db=db)

	@staticmethod
	async def get_by_event(event_id: str, db=None) -> List[dict]:
		db = db if db is not None else get_database()
		cursor = BookingModel.collection(db).find({"event_id": event_id})
		return await cursor.to_list(length=200)

__all__ = ["BookingModel"]
