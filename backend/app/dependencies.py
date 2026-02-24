"""
Dependency injections for FastAPI
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.db import get_database
from app.core.security import verify_token

security = HTTPBearer()


async def get_db():
    """Get database instance"""
    from app.db import db
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return payload
