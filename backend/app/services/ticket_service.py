# backend/app/services/ticket_service.py

from fastapi import HTTPException, status
from datetime import datetime
from app.models.ticket_model import TicketModel


class TicketService:

    # -----------------------------
    # Get Tickets By Booking
    # -----------------------------
    @staticmethod
    async def get_tickets_by_booking(booking_id: str):

        tickets = await TicketModel.get_by_booking(booking_id)

        if not tickets:
            raise HTTPException(
                status_code=404,
                detail="No tickets found for this booking"
            )

        return tickets

    # -----------------------------
    # Get Tickets By User
    # -----------------------------
    @staticmethod
    async def get_user_tickets(user_id: str):

        tickets = await TicketModel.get_by_user(user_id)

        return tickets

    # -----------------------------
    # Get Single Ticket
    # -----------------------------
    @staticmethod
    async def get_ticket(ticket_id: str):

        ticket = await TicketModel.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        return ticket

    # -----------------------------
    # Validate Ticket (QR Scan)
    # -----------------------------
    @staticmethod
    async def validate_ticket(ticket_code: str):

        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code"
            }

        if ticket["status"] == "cancelled":
            return {
                "valid": False,
                "message": "Ticket is cancelled"
            }

        if ticket["status"] == "used":
            return {
                "valid": False,
                "message": "Ticket already used"
            }

        # Mark as used
        await TicketModel.update_ticket(
            ticket["_id"],
            {
                "status": "used",
                "updated_at": datetime.utcnow()
            }
        )

        return {
            "valid": True,
            "message": "Ticket validated successfully",
            "ticket_id": str(ticket["_id"])
        }

    # -----------------------------
    # Cancel Ticket (Admin/System)
    # -----------------------------
    @staticmethod
    async def cancel_ticket(ticket_id: str):

        ticket = await TicketModel.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        if ticket["status"] == "used":
            raise HTTPException(
                status_code=400,
                detail="Used ticket cannot be cancelled"
            )

        await TicketModel.update_ticket(
            ticket_id,
            {
                "status": "cancelled",
                "updated_at": datetime.utcnow()
            }
        )

        return {"message": "Ticket cancelled successfully"}