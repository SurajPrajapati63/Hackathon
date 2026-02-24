# backend/app/routes/admin_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.roles import UserRole
from app.dependencies import get_current_user
from app.services.venue_service import VenueService
from app.services.refund_service import RefundService
from app.services.support_service import SupportService
from app.models.user_model import UserModel
from app.models.booking_model import BookingModel


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# -----------------------------
# Helper: Admin Role Check
# -----------------------------
def require_admin(user: dict):
    if user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# -----------------------------
# Get All Users
# -----------------------------
@router.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    users = await UserModel.collection.find().to_list(length=200)
    return users


# -----------------------------
# Create Venue
# -----------------------------
@router.post("/venues")
async def create_venue(data: dict, current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await VenueService.create_venue(data)


# -----------------------------
# Approve Refund
# -----------------------------
@router.put("/refunds/{refund_id}/approve")
async def approve_refund(refund_id: str, current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await RefundService.approve_refund(refund_id)


# -----------------------------
# Reject Refund
# -----------------------------
@router.put("/refunds/{refund_id}/reject")
async def reject_refund(refund_id: str, data: dict, current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await RefundService.reject_refund(refund_id, data.get("admin_note"))


# -----------------------------
# Get All Bookings
# -----------------------------
@router.get("/bookings")
async def get_all_bookings(current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    bookings = await BookingModel.collection.find().to_list(length=200)
    return bookings


# -----------------------------
# Get All Support Tickets
# -----------------------------
@router.get("/support")
async def get_all_support_tickets(current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await SupportService.get_all_tickets()