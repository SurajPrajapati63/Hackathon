"""
Authentication Router
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["authentication"])


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str
    role: str = "customer"


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user: UserRegister):
    """Register a new user"""
    return {
        "message": "User registered successfully",
        "access_token": "placeholder_token",
        "user": {"email": user.email, "role": user.role}
    }


@router.post("/login")
async def login(credentials: UserLogin):
    """Login user"""
    return {
        "message": "Login successful",
        "access_token": "placeholder_token",
        "user": {"email": credentials.username}
    }


@router.post("/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user():
    """Get current user info"""
    return {"email": "user@example.com", "role": "customer"}
