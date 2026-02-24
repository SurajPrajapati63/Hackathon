# backend/app/routes/customer_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.core.roles import UserRole
from app.services.event_service import EventService
from app.services.booking_service import BookingService
from app.services.ticket_service import TicketService
from app.services.refund_service import RefundService
from app.services.support_service import SupportService
from app.schemas.booking_schema import BookingCreate
from app.schemas.support_schema import SupportCreate
from app.schemas.refund_schema import RefundCreate
from app.models.booking_model import BookingModel
from app.services.auth_services import AuthService
from app.schemas.user_schemas import UserRegister, UserLogin


router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


# -----------------------------
# Role Check
# -----------------------------
def require_customer(user: dict):
    if user["role"] != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required"
        )


# -----------------------------
# View All Events
# -----------------------------
@router.get("/events")
async def get_events(current_user: dict = Depends(get_current_user)):

    require_customer(current_user)
    return await EventService.get_all_events()


# -----------------------------
# View Single Event
# -----------------------------
@router.get("/events/{event_id}")
async def get_event(event_id: str, current_user: dict = Depends(get_current_user)):

    require_customer(current_user)
    return await EventService.get_event(event_id)


# -----------------------------
# Create Booking (Lock Seats)
# -----------------------------
@router.post("/bookings")
async def create_booking(
    data: BookingCreate,
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await BookingService.create_booking(
        data,
        str(current_user["_id"])
    )


# -----------------------------
# Confirm Booking (After Payment)
# -----------------------------
@router.post("/bookings/{booking_id}/confirm")
async def confirm_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await BookingService.confirm_booking(
        booking_id,
        str(current_user["_id"])
    )


# -----------------------------
# View My Bookings
# -----------------------------
@router.get("/bookings")
async def get_my_bookings(current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    bookings = await BookingModel.get_by_user(str(current_user["_id"]))
    return bookings


# -----------------------------
# View Booking Summary
# -----------------------------
@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    return await BookingService.get_booking_summary(booking_id, str(current_user["_id"]))


# -----------------------------
# Cancel / Close Booking
# -----------------------------
@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    return await BookingService.cancel_booking(booking_id, str(current_user["_id"]))


# -----------------------------
# View My Tickets
# -----------------------------
@router.get("/tickets")
async def get_my_tickets(current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    return await TicketService.get_user_tickets(
        str(current_user["_id"])
    )


# -----------------------------
# View Available Seats for Event
# -----------------------------
@router.get("/events/{event_id}/seats")
async def get_event_seats(event_id: str, current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    from app.services.seat_service import SeatService

    return await SeatService.get_event_seats(event_id)


# -----------------------------
# View Single Ticket
# -----------------------------
@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str, current_user: dict = Depends(get_current_user)):

    require_customer(current_user)

    return await TicketService.get_ticket(ticket_id)


# -----------------------------
# Customer Signup
# -----------------------------
@router.post("/register")
async def customer_register(data: UserRegister):
    return await AuthService.register(data)


# -----------------------------
# Customer Login
# -----------------------------
@router.post("/login")
async def customer_login(data: UserLogin):
    return await AuthService.login(data)


# -----------------------------
# Request Refund
# -----------------------------
@router.post("/refunds")
async def request_refund(
    data: RefundCreate,
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await RefundService.request_refund(
        data.booking_id,
        data.reason,
        str(current_user["_id"])
    )


# -----------------------------
# Create Support Ticket
# -----------------------------
@router.post("/support")
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
# View My Support Tickets
# -----------------------------
@router.get("/support")
async def get_my_support_tickets(
    current_user: dict = Depends(get_current_user)
):

    require_customer(current_user)

    return await SupportService.get_user_tickets(
        str(current_user["_id"])
    )