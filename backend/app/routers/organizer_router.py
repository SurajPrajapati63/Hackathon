# backend/app/routes/organizer_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.core.roles import UserRole
from app.services.event_service import EventService
from app.services.entry_service import EntryService
from app.schemas.event_schema import EventCreate, EventUpdate
from app.models.booking_model import BookingModel
from app.services.seat_service import SeatService
from pydantic import BaseModel


# -----------------------------
# Seats Create Request
# -----------------------------
class SeatsCreateRequest(BaseModel):
    seat_numbers: list


router = APIRouter(
    prefix="/organizer",
    tags=["Organizer"]
)


# -----------------------------
# Role Check
# -----------------------------
def require_organizer(user: dict):
    if user["role"] not in [UserRole.ORGANIZER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer access required"
        )


# -----------------------------
# Create Event
# -----------------------------
@router.post("/events")
async def create_event(
    data: EventCreate,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await EventService.create_event(
        data,
        str(current_user["_id"])
    )


# -----------------------------
# Get My Events
# -----------------------------
@router.get("/events")
async def get_my_events(
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await EventService.get_organizer_events(
        str(current_user["_id"])
    )


# -----------------------------
# Update Event
# -----------------------------
@router.put("/events/{event_id}")
async def update_event(
    event_id: str,
    data: EventUpdate,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await EventService.update_event(
        event_id,
        data,
        current_user
    )


# -----------------------------
# Delete Event
# -----------------------------
@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await EventService.delete_event(
        event_id,
        current_user
    )


# -----------------------------
# View Bookings for My Events
# -----------------------------
@router.get("/events/{event_id}/bookings")
async def get_event_bookings(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    # Optional: You can verify event ownership here

    bookings = await BookingModel.get_by_event(event_id)
    return bookings


# -----------------------------
# View Entry Logs for Event
# -----------------------------
@router.get("/events/{event_id}/entries")
async def get_event_entries(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await EntryService.get_event_entries(event_id)


# -----------------------------
# Create Seats for Event
# -----------------------------
@router.post("/events/{event_id}/seats")
async def create_event_seats(
    event_id: str,
    data: SeatsCreateRequest,
    current_user: dict = Depends(get_current_user)
):

    require_organizer(current_user)

    return await SeatService.create_seats(event_id, data.seat_numbers)