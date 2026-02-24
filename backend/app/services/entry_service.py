# backend/app/services/entry_service.py

from fastapi import HTTPException
from datetime import datetime
from app.models.ticket_model import TicketModel
from app.models.entry_log_model import EntryLogModel
from app.models.event_model import EventModel


class EntryService:

    # =============================
    # TICKET VALIDATION
    # =============================

    # Check Ticket Validity (Without Marking as Used)
    # -----
    @staticmethod
    async def check_ticket_validity(ticket_code: str):
        """Check if a ticket is valid without marking it as used."""

        # 1️⃣ Check ticket exists
        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code",
                "ticket_id": None,
                "seat_number": None,
                "event_id": None,
                "ticket_status": None
            }

        # 2️⃣ Check ticket status
        if ticket["status"] == "cancelled":
            return {
                "valid": False,
                "message": "Ticket is cancelled",
                "ticket_id": str(ticket["_id"]),
                "seat_number": ticket.get("seat_number"),
                "event_id": ticket["event_id"],
                "ticket_status": "cancelled"
            }

        if ticket["status"] == "used":
            return {
                "valid": False,
                "message": "Ticket already used",
                "ticket_id": str(ticket["_id"]),
                "seat_number": ticket.get("seat_number"),
                "event_id": ticket["event_id"],
                "ticket_status": "used"
            }

        # 3️⃣ Check event date
        event = await EventModel.get_by_id(ticket["event_id"])

        if not event:
            return {
                "valid": False,
                "message": "Event not found",
                "ticket_id": str(ticket["_id"]),
                "seat_number": ticket.get("seat_number"),
                "event_id": ticket["event_id"],
                "ticket_status": ticket["status"]
            }

        if event["event_date"] < datetime.utcnow():
            return {
                "valid": False,
                "message": "Event has already ended",
                "ticket_id": str(ticket["_id"]),
                "seat_number": ticket.get("seat_number"),
                "event_id": ticket["event_id"],
                "ticket_status": ticket["status"],
                "event_date": event.get("event_date")
            }

        # Ticket is valid
        return {
            "valid": True,
            "message": "Ticket is valid",
            "ticket_id": str(ticket["_id"]),
            "seat_number": ticket.get("seat_number"),
            "event_id": ticket["event_id"],
            "ticket_status": ticket["status"],
            "event_date": event.get("event_date"),
            "event_title": event.get("title"),
            "booking_id": ticket.get("booking_id")
        }

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

    # =============================
    # ADDITIONAL ENTRY MANAGEMENT
    # =============================

    # Mark Ticket as Unread
    # (Reset from "used" back to "active")
    # -----
    @staticmethod
    async def mark_ticket_unread(ticket_code: str, staff_id: str):

        # 1️⃣ Check ticket exists
        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code"
            }

        # 2️⃣ Check ticket status is "used"
        if ticket["status"] != "used":
            return {
                "valid": False,
                "message": "Ticket is not marked as used"
            }

        # 3️⃣ Mark ticket as active (unread)
        await TicketModel.update_ticket(
            ticket["_id"],
            {
                "status": "active",
                "updated_at": datetime.utcnow()
            }
        )

        return {
            "valid": True,
            "message": "Ticket marked as unread (active)",
            "ticket_id": str(ticket["_id"]),
            "seat_number": ticket["seat_number"]
        }

    # Reject Invalid Ticket
    # -----
    @staticmethod
    async def reject_invalid_ticket(ticket_code: str, staff_id: str, reason: str = None):

        # 1️⃣ Check ticket exists
        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code"
            }

        # 2️⃣ Check if already cancelled
        if ticket["status"] == "cancelled":
            return {
                "valid": False,
                "message": "Ticket is already cancelled"
            }

        # 3️⃣ Mark ticket as cancelled
        await TicketModel.update_ticket(
            ticket["_id"],
            {
                "status": "cancelled",
                "rejection_reason": reason or "Rejected at gate",
                "rejected_by": staff_id,
                "rejected_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )

        # 4️⃣ Create rejection log
        rejection_log = {
            "ticket_id": str(ticket["_id"]),
            "event_id": ticket["event_id"],
            "rejected_by": staff_id,
            "rejection_time": datetime.utcnow(),
            "rejection_reason": reason or "Rejected at gate",
        }

        await EntryLogModel.create_entry(rejection_log)

        return {
            "valid": False,
            "message": "Ticket rejected and cancelled",
            "ticket_id": str(ticket["_id"]),
            "reason": reason or "Rejected at gate"
        }

    # Reject Already Used Ticket
    # -----
    @staticmethod
    async def reject_used_ticket(ticket_code: str, staff_id: str):

        # 1️⃣ Check ticket exists
        ticket = await TicketModel.get_by_code(ticket_code)

        if not ticket:
            return {
                "valid": False,
                "message": "Invalid ticket code"
            }

        # 2️⃣ Check if already used
        if ticket["status"] != "used":
            return {
                "valid": False,
                "message": "Ticket is not marked as used"
            }

        # 3️⃣ Create duplicate entry log
        duplicate_log = {
            "ticket_id": str(ticket["_id"]),
            "event_id": ticket["event_id"],
            "rejected_by": staff_id,
            "rejection_time": datetime.utcnow(),
            "rejection_reason": "Duplicate entry attempt - ticket already used",
        }

        await EntryLogModel.create_entry(duplicate_log)

        return {
            "valid": False,
            "message": "Ticket already used - duplicate entry rejected",
            "ticket_id": str(ticket["_id"]),
            "seat_number": ticket["seat_number"]
        }