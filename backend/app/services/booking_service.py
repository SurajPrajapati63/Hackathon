# backend/app/services/booking_service.py

from fastapi import HTTPException, status
from datetime import datetime
from app.models.booking_model import BookingModel
from app.models.event_model import EventModel
from app.models.ticket_model import TicketModel
from app.services.seat_service import SeatService
from app.schemas.booking_schema import BookingCreate
import uuid


class BookingService:

    # -----------------------------
    # Create Booking (Lock Seats)
    # -----------------------------
    @staticmethod
    async def create_booking(data: BookingCreate, user_id: str):

        # 1️⃣ Check Event Exists
        event = await EventModel.get_by_id(data.event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        # 2️⃣ Lock Seats
        await SeatService.lock_seats(
            data.event_id,
            data.seat_numbers,
            user_id
        )

        # 3️⃣ Calculate Total Amount
        total_amount = event["ticket_price"] * len(data.seat_numbers)

        # 4️⃣ Create Booking
        booking_data = {
            "user_id": user_id,
            "event_id": data.event_id,
            "seat_numbers": data.seat_numbers,
            "total_amount": total_amount,
            "booking_status": "pending",
            "payment_status": "unpaid",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        booking_id = await BookingModel.create_booking(booking_data)

        return {
            "message": "Seats locked. Proceed to payment.",
            "booking_id": booking_id,
            "total_amount": total_amount
        }

    # -----------------------------
    # Confirm Booking (After Payment)
    # -----------------------------
    @staticmethod
    async def confirm_booking(booking_id: str, user_id: str):

        booking = await BookingModel.get_by_id(booking_id)

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        if booking["booking_status"] != "pending":
            raise HTTPException(
                status_code=400,
                detail="Booking already processed"
            )

        # 1️⃣ Confirm Seats
        await SeatService.confirm_seats(
            booking["event_id"],
            booking["seat_numbers"],
            user_id
        )

        # 2️⃣ Update Booking Status
        await BookingModel.update_booking(
            booking_id,
            {
                "booking_status": "confirmed",
                "payment_status": "paid",
                "updated_at": datetime.utcnow()
            }
        )

        # 3️⃣ Generate Tickets
        tickets = []

        for seat in booking["seat_numbers"]:

            ticket_code = f"TKT-{uuid.uuid4().hex[:10].upper()}"

            ticket_data = {
                "booking_id": booking_id,
                "user_id": user_id,
                "event_id": booking["event_id"],
                "seat_number": seat,
                "ticket_code": ticket_code,
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            ticket_id = await TicketModel.create_ticket(ticket_data)

            tickets.append({
                "ticket_id": ticket_id,
                "seat": seat,
                "ticket_code": ticket_code
            })

        return {
            "message": "Booking confirmed successfully",
            "tickets": tickets
        }

    # -----------------------------
    # Get Booking Summary
    # -----------------------------
    @staticmethod
    async def get_booking_summary(booking_id: str, user_id: str):

        booking = await BookingModel.get_by_id(booking_id)

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        # Build summary
        summary = {
            "booking_id": booking_id,
            "user_id": booking["user_id"],
            "event_id": booking["event_id"],
            "seat_numbers": booking["seat_numbers"],
            "total_amount": booking.get("total_amount"),
            "booking_status": booking.get("booking_status"),
            "payment_status": booking.get("payment_status"),
            "created_at": booking.get("created_at"),
            "updated_at": booking.get("updated_at")
        }

        return summary

    # -----------------------------
    # Cancel Booking
    # -----------------------------
    @staticmethod
    async def cancel_booking(booking_id: str, user_id: str):

        booking = await BookingModel.get_by_id(booking_id)

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if booking["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        if booking["booking_status"] != "confirmed":
            raise HTTPException(
                status_code=400,
                detail="Only confirmed bookings can be cancelled"
            )

        # Release Seats
        for seat_number in booking["seat_numbers"]:
            await SeatService.release_expired_locks()

        await BookingModel.update_booking(
            booking_id,
            {
                "booking_status": "cancelled",
                "payment_status": "refunded",
                "updated_at": datetime.utcnow()
            }
        )

        return {"message": "Booking cancelled successfully"}