# backend/app/schemas/booking_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Booking Status Enum
# -----------------------------
class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REFUNDED = "refunded"


# -----------------------------
# Payment Status Enum
# -----------------------------
class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


# -----------------------------
# Base Booking Schema
# -----------------------------
class BookingBase(BaseModel):
    event_id: str
    seat_numbers: List[str] = Field(..., min_length=1)
    total_amount: float = Field(..., gt=0)


# -----------------------------
# Create Booking Schema
# -----------------------------
class BookingCreate(BaseModel):
    event_id: str
    seat_numbers: List[str] = Field(..., min_length=1)


# -----------------------------
# Update Booking Schema
# -----------------------------
class BookingUpdate(BaseModel):
    booking_status: Optional[BookingStatus] = None
    payment_status: Optional[PaymentStatus] = None


# -----------------------------
# Booking Response Schema
# -----------------------------
class BookingResponse(BaseModel):
    id: str
    user_id: str
    event_id: str
    seat_numbers: List[str]
    total_amount: float
    booking_status: BookingStatus
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True