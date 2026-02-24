# backend/app/services/refund_service.py

from fastapi import HTTPException, status
from datetime import datetime
from app.models.refund_model import RefundModel
from app.models.booking_model import BookingModel
from app.models.ticket_model import TicketModel


class RefundService:

    # -----------------------------
    # Create Refund Request
    # -----------------------------
    @staticmethod
    async def request_refund(booking_id: str, reason: str, user_id: str):

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
                detail="Only confirmed bookings can be refunded"
            )

        # Check if refund already exists
        existing_refund = await RefundModel.get_by_booking(booking_id)
        if existing_refund:
            raise HTTPException(
                status_code=400,
                detail="Refund already requested for this booking"
            )

        refund_data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "refund_amount": booking["total_amount"],
            "reason": reason,
            "status": "requested",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        refund_id = await RefundModel.create_refund(refund_data)

        return {
            "message": "Refund request submitted successfully",
            "refund_id": refund_id
        }

    # -----------------------------
    # Approve Refund (Admin)
    # -----------------------------
    @staticmethod
    async def approve_refund(refund_id: str):

        refund = await RefundModel.get_by_id(refund_id)

        if not refund:
            raise HTTPException(
                status_code=404,
                detail="Refund not found"
            )

        if refund["status"] != "requested":
            raise HTTPException(
                status_code=400,
                detail="Refund already processed"
            )

        booking = await BookingModel.get_by_id(refund["booking_id"])

        # Update refund status
        await RefundModel.update_refund(
            refund_id,
            {
                "status": "processed",
                "updated_at": datetime.utcnow()
            }
        )

        # Update booking status
        await BookingModel.update_booking(
            refund["booking_id"],
            {
                "booking_status": "cancelled",
                "payment_status": "refunded",
                "updated_at": datetime.utcnow()
            }
        )

        # Cancel all tickets
        tickets = await TicketModel.get_by_booking(refund["booking_id"])

        for ticket in tickets:
            await TicketModel.update_ticket(
                ticket["_id"],
                {
                    "status": "cancelled",
                    "updated_at": datetime.utcnow()
                }
            )

        return {"message": "Refund approved and processed successfully"}

    # -----------------------------
    # Reject Refund (Admin)
    # -----------------------------
    @staticmethod
    async def reject_refund(refund_id: str, admin_note: str):

        refund = await RefundModel.get_by_id(refund_id)

        if not refund:
            raise HTTPException(
                status_code=404,
                detail="Refund not found"
            )

        if refund["status"] != "requested":
            raise HTTPException(
                status_code=400,
                detail="Refund already processed"
            )

        await RefundModel.update_refund(
            refund_id,
            {
                "status": "rejected",
                "admin_note": admin_note,
                "updated_at": datetime.utcnow()
            }
        )

        return {"message": "Refund rejected successfully"}

    # -----------------------------
    # Get Refund by Booking
    # -----------------------------
    @staticmethod
    async def get_refund_by_booking(booking_id: str):

        refund = await RefundModel.get_by_booking(booking_id)

        if not refund:
            raise HTTPException(
                status_code=404,
                detail="No refund found"
            )

        return refund