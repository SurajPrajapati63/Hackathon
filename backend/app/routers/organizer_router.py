"""
Organizer Router
"""
from fastapi import APIRouter

router = APIRouter(prefix="/organizer", tags=["organizer"])


@router.get("/dashboard")
async def get_organizer_dashboard():
    """Get organizer dashboard"""
    return {"data": {}}
