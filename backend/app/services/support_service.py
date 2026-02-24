# backend/app/services/support_service.py

from fastapi import HTTPException, status
from datetime import datetime
from app.models.support_model import SupportModel
from app.models.booking_model import BookingModel


class SupportService:

    # -----------------------------
    # Create Support Ticket
    # -----------------------------
    @staticmethod
    async def create_ticket(data: dict, user_id: str):

        # Optional: Validate booking if provided
        if data.get("booking_id"):
            booking = await BookingModel.get_by_id(data["booking_id"])
            if not booking:
                raise HTTPException(
                    status_code=404,
                    detail="Booking not found"
                )

        ticket_data = {
            "user_id": user_id,
            "subject": data["subject"],
            "description": data["description"],
            "category": data["category"],
            "booking_id": data.get("booking_id"),
            "status": "open",
            "admin_response": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        ticket_id = await SupportModel.create_ticket(ticket_data)

        return {
            "message": "Support ticket created successfully",
            "ticket_id": ticket_id
        }

    # -----------------------------
    # Get Tickets for Logged-in User
    # -----------------------------
    @staticmethod
    async def get_user_tickets(user_id: str):

        tickets = await SupportModel.get_by_user(user_id)

        return tickets

    # -----------------------------
    # Get All Tickets (Admin)
    # -----------------------------
    @staticmethod
    async def get_all_tickets():

        tickets = await SupportModel.get_all()

        return tickets

    # -----------------------------
    # Get Single Ticket
    # -----------------------------
    @staticmethod
    async def get_ticket(ticket_id: str, user_id: str, role: str):

        ticket = await SupportModel.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        # Only owner or admin can view
        if ticket["user_id"] != user_id and role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Unauthorized access"
            )

        return ticket

    # -----------------------------
    # Update Ticket (Admin Only)
    # -----------------------------
    @staticmethod
    async def update_ticket(ticket_id: str, update_data: dict):

        ticket = await SupportModel.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        await SupportModel.update_ticket(
            ticket_id,
            {
                **update_data,
                "updated_at": datetime.utcnow()
            }
        )

        return {"message": "Support ticket updated successfully"}

    # -----------------------------
    # Close Ticket (User)
    # -----------------------------
    @staticmethod
    async def close_ticket(ticket_id: str, user_id: str):

        ticket = await SupportModel.get_by_id(ticket_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        if ticket["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized"
            )

        await SupportModel.update_ticket(
            ticket_id,
            {
                "status": "closed",
                "updated_at": datetime.utcnow()
            }
        )

        return {"message": "Ticket closed successfully"}