# backend/app/schemas/refund_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Refund Status Enum
# -----------------------------
class RefundStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSED = "processed"
    FAILED = "failed"


# -----------------------------
# Base Refund Schema
# -----------------------------
class RefundBase(BaseModel):
    booking_id: str
    reason: str = Field(..., min_length=5, max_length=500)


# -----------------------------
# Create Refund Request
# -----------------------------
class RefundCreate(RefundBase):
    pass


# -----------------------------
# Admin Update Refund
# -----------------------------
class RefundUpdate(BaseModel):
    status: Optional[RefundStatus] = None
    admin_note: Optional[str] = None


# -----------------------------
# Refund Response Schema
# -----------------------------
class RefundResponse(BaseModel):
    id: str
    booking_id: str
    user_id: str
    refund_amount: float
    reason: str
    status: RefundStatus
    admin_note: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True