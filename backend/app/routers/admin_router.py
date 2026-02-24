"""
Admin Router
"""
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def get_all_users():
    """Get all users (admin only)"""
    return {"data": []}


@router.get("/statistics")
async def get_statistics():
    """Get system statistics (admin only)"""
    return {"data": {}}
