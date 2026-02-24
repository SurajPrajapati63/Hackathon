# backend/app/schemas/event_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Event Status Enum
# -----------------------------
class EventStatus(str, Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


# -----------------------------
# Base Schema (Common Fields)
# -----------------------------
class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    category: str = Field(..., min_length=3)
    venue_id: str
    event_date: datetime
    ticket_price: float = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)


# -----------------------------
# Create Event Schema
# -----------------------------
class EventCreate(EventBase):
    pass


# -----------------------------
# Update Event Schema
# -----------------------------
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    event_date: Optional[datetime] = None
    ticket_price: Optional[float] = Field(None, gt=0)
    total_seats: Optional[int] = Field(None, gt=0)
    status: Optional[EventStatus] = None


# -----------------------------
# Event Response Schema
# -----------------------------
class EventResponse(EventBase):
    id: str
    organizer_id: str
    tickets_sold: int
    status: EventStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True