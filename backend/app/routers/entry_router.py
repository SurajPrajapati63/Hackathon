# backend/app/routes/entry_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.services.entry_service import EntryService
from app.core.roles import UserRole
from pydantic import BaseModel


router = APIRouter(
    prefix="/entry",
    tags=["Entry Management"]
)


# -----------------------------
# Request Schema
# -----------------------------
class EntryValidationRequest(BaseModel):
    ticket_code: str
    device_info: str | None = None


# -----------------------------
# Role Check (Admin / Organizer)
# -----------------------------
def require_entry_access(user: dict):
    if user["role"] not in [UserRole.ADMIN, UserRole.ORGANIZER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Entry access restricted to Admin or Organizer"
        )


# -----------------------------
# Validate Ticket (Gate Scan)
# -----------------------------
@router.post("/validate")
async def validate_ticket(
    data: EntryValidationRequest,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.validate_entry(
        ticket_code=data.ticket_code,
        staff_id=str(current_user["_id"]),
        device_info=data.device_info
    )


# -----------------------------
# Get All Entries for Event
# -----------------------------
@router.get("/event/{event_id}")
async def get_event_entries(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.get_event_entries(event_id)


# -----------------------------
# Get Entry Logs for Ticket
# -----------------------------
@router.get("/ticket/{ticket_id}")
async def get_ticket_entries(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.get_ticket_entries(ticket_id)