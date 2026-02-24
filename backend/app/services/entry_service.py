# backend/app/services/entry_service.py

from fastapi import HTTPException
from datetime import datetime
from app.models.ticket_model import TicketModel
from app.models.entry_log_model import EntryLogModel
from app.models.event_model import EventModel


class EntryService:

    # -----------------------------
    # Validate Ticket & Allow Entry
    # -----------------------------
    @staticmethod
    async def validate_entry(ticket_code: str, staff_id: str, device_info: str = None):

        # 1️⃣ Check ticket exists
        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code"
            }

        # 2️⃣ Check ticket status
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

        # 3️⃣ Check event date (optional validation)
        event = await EventModel.get_by_id(ticket["event_id"])

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event["event_date"] < datetime.utcnow():
            return {
                "valid": False,
                "message": "Event has already ended"
            }

        # 4️⃣ Mark ticket as used
        await TicketModel.update_ticket(
            ticket["_id"],
            {
                "status": "used",
                "updated_at": datetime.utcnow()
            }
        )

        # 5️⃣ Create entry log
        entry_log = {
            "ticket_id": str(ticket["_id"]),
            "event_id": ticket["event_id"],
            "validated_by": staff_id,
            "entry_time": datetime.utcnow(),
            "device_info": device_info,
        }

        await EntryLogModel.create_entry(entry_log)

        return {
            "valid": True,
            "message": "Entry allowed",
            "ticket_id": str(ticket["_id"]),
            "seat_number": ticket["seat_number"]
        }

    # -----------------------------
    # Get Entry Logs for Event
    # -----------------------------
    @staticmethod
    async def get_event_entries(event_id: str):

        logs = await EntryLogModel.get_by_event(event_id)
        return logs

    # -----------------------------
    # Get Entry Logs by Ticket
    # -----------------------------
    @staticmethod
    async def get_ticket_entries(ticket_id: str):

        logs = await EntryLogModel.get_by_ticket(ticket_id)
        return logs