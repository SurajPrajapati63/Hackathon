# backend/app/schemas/ticket_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Ticket Status Enum
# -----------------------------
class TicketStatus(str, Enum):
    ACTIVE = "active"
    USED = "used"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# -----------------------------
# Base Ticket Schema
# -----------------------------
class TicketBase(BaseModel):
    booking_id: str
    event_id: str
    seat_number: str = Field(..., min_length=1)
    ticket_code: str  # Unique code for QR / validation


# -----------------------------
# Create Ticket Schema
# (Usually internal use only)
# -----------------------------
class TicketCreate(TicketBase):
    pass


# -----------------------------
# Ticket Response Schema
# -----------------------------
class TicketResponse(BaseModel):
    id: str
    booking_id: str
    user_id: str
    event_id: str
    seat_number: str
    ticket_code: str
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Ticket Validation Schema
# (For Entry Gate)
# -----------------------------
class TicketValidationRequest(BaseModel):
    ticket_code: str


class TicketValidationResponse(BaseModel):
    valid: bool
    message: str
    ticket_id: Optional[str] = None