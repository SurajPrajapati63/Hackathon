# backend/app/routes/entry_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.services.entry_service import EntryService
from app.core.roles import UserRole
from pydantic import BaseModel
from app.services.auth_services import AuthService
from app.schemas.user_schemas import UserLogin



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


class TicketRejectionRequest(BaseModel):
    ticket_code: str
    reason: str | None = None


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
# (Mark as Used + Create Log)
# -----
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


# Check Ticket Validity
# (Without Marking as Used)
# -----
@router.post("/check-validity")
async def check_ticket_validity(
    data: EntryValidationRequest,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.check_ticket_validity(
        ticket_code=data.ticket_code
    )


# -----------------------------
# Entry Manager Login
# -----------------------------
@router.post("/login")
async def entry_login(login_data: UserLogin):
    """Login endpoint for entry managers (Admin or Organizer only)."""
    resp = await AuthService.login(login_data)

    user = resp.get("user")
    if not user or user.get("role") not in [UserRole.ADMIN.value, UserRole.ORGANIZER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Entry access restricted to Admin or Organizer"
        )

    return resp


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


# =============================
# TICKET MANAGEMENT (Entry)
# =============================

# Mark Ticket as Unread
# (Reset from "used" back to "active")
# -----
@router.post("/mark-unread")
async def mark_ticket_unread(
    data: EntryValidationRequest,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.mark_ticket_unread(
        ticket_code=data.ticket_code,
        staff_id=str(current_user["_id"])
    )


# Reject Invalid Ticket
# -----
@router.post("/reject-invalid")
async def reject_invalid_ticket(
    data: TicketRejectionRequest,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.reject_invalid_ticket(
        ticket_code=data.ticket_code,
        staff_id=str(current_user["_id"]),
        reason=data.reason
    )


# Reject Already Used Ticket
# -----
@router.post("/reject-used")
async def reject_used_ticket(
    data: EntryValidationRequest,
    current_user: dict = Depends(get_current_user)
):

    require_entry_access(current_user)

    return await EntryService.reject_used_ticket(
        ticket_code=data.ticket_code,
        staff_id=str(current_user["_id"])
    )