# backend/app/schemas/support_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Support Ticket Status Enum
# -----------------------------
class SupportStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


# -----------------------------
# Support Category Enum
# -----------------------------
class SupportCategory(str, Enum):
    BOOKING = "booking"
    PAYMENT = "payment"
    REFUND = "refund"
    EVENT = "event"
    OTHER = "other"


# -----------------------------
# Base Support Schema
# -----------------------------
class SupportBase(BaseModel):
    subject: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    category: SupportCategory
    booking_id: Optional[str] = None


# -----------------------------
# Create Support Ticket
# -----------------------------
class SupportCreate(SupportBase):
    pass


# -----------------------------
# Admin Update Ticket
# -----------------------------
class SupportUpdate(BaseModel):
    status: Optional[SupportStatus] = None
    admin_response: Optional[str] = None


# -----------------------------
# Support Response Schema
# -----------------------------
class SupportResponse(BaseModel):
    id: str
    user_id: str
    subject: str
    description: str
    category: SupportCategory
    booking_id: Optional[str]
    status: SupportStatus
    admin_response: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True