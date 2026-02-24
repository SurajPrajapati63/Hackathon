# backend/app/routes/support_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.dependencies import get_current_user
from app.core.roles import UserRole
from app.services.support_service import SupportService
from app.services.refund_service import RefundService
from app.schemas.support_schema import SupportCreate, SupportUpdate, ResolutionNoteCreate


router = APIRouter(
    prefix="/support",
    tags=["Support"]
)


# -----------------------------
# Role Helpers
# -----------------------------
def require_customer(user: dict):
    if user["role"] != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required"
        )


def require_admin(user: dict):
    if user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# -----------------------------
# Create Support Ticket (Customer)
# -----------------------------
@router.post("/")
async def create_support_ticket(
    data: SupportCreate,
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await SupportService.create_ticket(
        data.model_dump(),
        str(current_user["_id"])
    )


# -----------------------------
# Get My Support Tickets (Customer)
# -----------------------------
@router.get("/me")
async def get_my_support_tickets(
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await SupportService.get_user_tickets(
        str(current_user["_id"])
    )


# -----------------------------
# Close Ticket (Customer)
# -----------------------------
@router.put("/{ticket_id}/close")
async def close_ticket(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await SupportService.close_ticket(
        ticket_id,
        str(current_user["_id"])
    )


# -----------------------------
# Get All Support Tickets (Admin)
# -----------------------------
@router.get("/admin")
async def get_all_tickets(
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    return await SupportService.get_all_tickets()


# -----------------------------
# Update Ticket (Admin)
# -----------------------------
@router.put("/admin/{ticket_id}")
async def update_ticket(
    ticket_id: str,
    data: SupportUpdate,
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    return await SupportService.update_ticket(
        ticket_id,
        data.model_dump(exclude_none=True)
    )


# =============================
# REFUND MANAGEMENT (Support Executive)
# =============================

# Approve Refund
# -----------------------------
@router.put("/refunds/{refund_id}/approve")
async def approve_refund(refund_id: str, current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await RefundService.approve_refund(refund_id)


# Reject Refund
# -----------------------------
class RefundRejectData(BaseModel):
    admin_note: str = None


# Reject Refund
# -----------------------------
class RefundRejectData(BaseModel):
    admin_note: str = None


@router.put("/refunds/{refund_id}/reject")
async def reject_refund(
    refund_id: str,
    data: RefundRejectData,
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    return await RefundService.reject_refund(refund_id, data.admin_note)


# =============================
# RESOLUTION NOTES MANAGEMENT
# =============================

# Add Resolution Note
# -----
@router.post("/{ticket_id}/notes")
async def add_resolution_note(
    ticket_id: str,
    data: ResolutionNoteCreate,
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    user_name = current_user.get("name", current_user.get("email", "Admin"))

    return await SupportService.add_resolution_note(
        ticket_id,
        data.note,
        str(current_user["_id"]),
        user_name
    )


# Get Resolution Notes
# -----
@router.get("/{ticket_id}/notes")
async def get_resolution_notes(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):

    return await SupportService.get_resolution_notes(
        ticket_id,
        str(current_user["_id"]),
        current_user["role"]
    )


# Delete Resolution Note
# -----
class DeleteNoteRequest(BaseModel):
    note_index: int


@router.delete("/{ticket_id}/notes/{note_index}")
async def delete_resolution_note(
    ticket_id: str,
    note_index: int,
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    return await SupportService.delete_resolution_note(
        ticket_id,
        note_index,
        str(current_user["_id"])
    )