"""
Entry Router
"""
from fastapi import APIRouter

router = APIRouter(prefix="/entry", tags=["entry"])


@router.post("/validate")
async def validate_entry():
    """Validate ticket for entry"""
    return {"valid": True}
