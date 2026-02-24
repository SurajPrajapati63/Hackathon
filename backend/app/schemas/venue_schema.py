# backend/app/schemas/venue_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -----------------------------
# Base Schema
# -----------------------------
class VenueBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    location: str = Field(..., min_length=3, max_length=200)
    capacity: int = Field(..., gt=0)
    description: Optional[str] = None


# -----------------------------
# Create Schema
# -----------------------------
class VenueCreate(VenueBase):
    pass


# -----------------------------
# Update Schema
# -----------------------------
class VenueUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None


# -----------------------------
# Response Schema
# -----------------------------
class VenueResponse(VenueBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True