"""
Customer Router
"""
from fastapi import APIRouter

router = APIRouter(prefix="/customer", tags=["customer"])


@router.get("/dashboard")
async def get_customer_dashboard():
    """Get customer dashboard"""
    return {"data": {}}
