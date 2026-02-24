# backend/app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# -----------------------------
# Role Enum
# -----------------------------
class UserRole(str, Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    CUSTOMER = "customer"


# -----------------------------
# Base Schema (Common Fields)
# -----------------------------
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    role: UserRole = UserRole.CUSTOMER


# -----------------------------
# Register Schema (Request)
# -----------------------------
class UserRegister(UserBase):
    password: str = Field(..., min_length=6)


# -----------------------------
# Login Schema (Request)
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# Update Schema
# -----------------------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


# -----------------------------
# Database Schema (Internal)
# -----------------------------
class UserInDB(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# Response Schema (Safe Output)
# -----------------------------
class UserResponse(UserInDB):
    pass


# -----------------------------
# Auth Response Schema
# -----------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse