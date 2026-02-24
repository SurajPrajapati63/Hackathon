# backend/app/services/seat_service.py

from fastapi import HTTPException, status
from datetime import datetime, timedelta
from bson import ObjectId
from app.models.seat_model import SeatModel


LOCK_DURATION_MINUTES = 5  # Seats locked for 5 minutes


class SeatService:

    # -----------------------------
    # Get All Seats for Event
    # -----------------------------
    @staticmethod
    async def get_event_seats(event_id: str):
        seats = await SeatModel.get_by_event(event_id)
        return seats

    # -----------------------------
    # Lock Seats (Before Payment)
    # -----------------------------
    @staticmethod
    async def lock_seats(event_id: str, seat_numbers: list, user_id: str):

        locked_seats = []

        for seat_number in seat_numbers:

            seat = await SeatModel.get_by_event_and_seat(
                event_id, seat_number
            )

            if not seat:
                raise HTTPException(
                    status_code=404,
                    detail=f"Seat {seat_number} not found"
                )

            # If already booked
            if seat["status"] == "booked":
                raise HTTPException(
                    status_code=400,
                    detail=f"Seat {seat_number} already booked"
                )

            # If locked and not expired
            if seat["status"] == "locked" and seat.get("lock_expiry") > datetime.utcnow():
                raise HTTPException(
                    status_code=400,
                    detail=f"Seat {seat_number} is temporarily locked"
                )

            lock_expiry = datetime.utcnow() + timedelta(minutes=LOCK_DURATION_MINUTES)

            await SeatModel.update_seat(
                seat["_id"],
                {
                    "status": "locked",
                    "locked_by": user_id,
                    "lock_expiry": lock_expiry
                }
            )

            locked_seats.append(seat_number)

        return {
            "message": "Seats locked successfully",
            "locked_seats": locked_seats,
            "expires_in_minutes": LOCK_DURATION_MINUTES
        }

    # -----------------------------
    # Confirm Seats (After Payment Success)
    # -----------------------------
    @staticmethod
    async def confirm_seats(event_id: str, seat_numbers: list, user_id: str):

        for seat_number in seat_numbers:

            seat = await SeatModel.get_by_event_and_seat(
                event_id, seat_number
            )

            if not seat:
                raise HTTPException(
                    status_code=404,
                    detail=f"Seat {seat_number} not found"
                )

            if seat["status"] != "locked" or seat["locked_by"] != user_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Seat {seat_number} not locked by this user"
                )

            await SeatModel.update_seat(
                seat["_id"],
                {
                    "status": "booked",
                    "locked_by": None,
                    "lock_expiry": None
                }
            )

        return {"message": "Seats booked successfully"}

    # -----------------------------
    # Release Expired Locks
    # -----------------------------
    @staticmethod
    async def release_expired_locks():

        expired_seats = await SeatModel.get_expired_locks(datetime.utcnow())

        for seat in expired_seats:
            await SeatModel.update_seat(
                seat["_id"],
                {
                    "status": "available",
                    "locked_by": None,
                    "lock_expiry": None
                }
            )

        return {"released_seats": len(expired_seats)}