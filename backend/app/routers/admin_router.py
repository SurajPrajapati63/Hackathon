# backend/app/routes/admin_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.roles import UserRole
from app.dependencies import get_current_user
from app.services.venue_service import VenueService
from app.schemas.venue_schema import VenueCreate
from app.services.support_service import SupportService
from app.models.user_models import UserModel
from app.models.booking_model import BookingModel
from app.services.event_service import EventService
from app.schemas.event_schema import EventStatus, EventCreate


# Request model for event status update
class EventStatusUpdate(BaseModel):
    status: EventStatus


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
    users = await UserModel.collection().find().to_list(length=200)
    return users


# -----------------------------
# Create Venue
# -----------------------------
@router.post("/venues")
async def create_venue(data: VenueCreate, current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await VenueService.create_venue(data)


# -----------------------------
# Get All Bookings
# -----------------------------
@router.get("/bookings")
async def get_all_bookings(current_user: dict = Depends(get_current_user)):

    require_admin(current_user)
    bookings = await BookingModel.collection().find().to_list(length=200)
    return bookings


# -----------------------------
# Get All Support Tickets
# -----------------------------
@router.get("/support")
async def get_all_support_tickets(current_user: dict = Depends(get_current_user)):

    require_admin(current_user)

    return await SupportService.get_all_tickets()


# -----------------------------
# Update Event Status (Admin)
# -----------------------------
@router.put("/events/{event_id}/status")
async def update_event_status(
    event_id: str,
    data: EventStatusUpdate,
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    return await EventService.update_event(
        event_id,
        {"status": data.status.value},
        current_user
    )