from fastapi import HTTPException, status
from backend.app.db import get_db
from utils.hash import hash_password, verify_password
from utils.jwt_handler import create_access_token
from utils.logger import logger


async def register_user(user):
    db = get_db()

    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pwd = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd
    }

    await db.users.insert_one(new_user)

    logger.info(f"New user registered: {user.email}")

    return {"message": "User registered successfully"}


async def login_user(user):
    db = get_db()

    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": user.email})

    logger.info(f"User logged in: {user.email}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }