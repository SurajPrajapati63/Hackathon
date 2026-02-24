# backend/app/services/auth_service.py

from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user_models import UserModel
from app.schemas.user_schemas import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.core.constants import ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:

    # -----------------------------
    # Register User
    # -----------------------------
    @staticmethod
    async def register(user_data: UserRegister):

        # Check if email already exists
        existing_user = await UserModel.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        try:
            hashed_pwd = hash_password(user_data.password)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc)
            ) from exc

        user_dict = user_data.model_dump()
        user_dict["password"] = hashed_pwd

        user_id = await UserModel.create_user(user_dict)

        return {"message": "User registered successfully", "user_id": user_id}

    # -----------------------------
    # Login User
    # -----------------------------
    @staticmethod
    async def login(login_data: UserLogin):

        user = await UserModel.get_by_email(login_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        token = create_access_token(
            data={
                "sub": str(user["_id"]),
                "role": user["role"],
                "email": user["email"]
            },
            expires_delta=access_token_expires
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user.get("role"),
                "is_active": user.get("is_active", True),
                "is_verified": user.get("is_verified", False),
                "created_at": user.get("created_at"),
                "updated_at": user.get("updated_at")
            }
        }
