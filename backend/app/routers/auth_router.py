# backend/app/routes/auth_routes.py

from fastapi import APIRouter, status
from app.schemas.user_schemas import (
    UserRegister,
    UserLogin,
    TokenResponse
)
from app.services.auth_services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -----------------------------
# Register Endpoint
# -----------------------------
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserRegister):
    """
    Register a new user
    """
    return await AuthService.register(user_data)


# -----------------------------
# Login Endpoint
# -----------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(login_data: UserLogin):
    """
    Login user and return JWT token
    """
    return await AuthService.login(login_data)