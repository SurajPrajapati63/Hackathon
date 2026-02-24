"""
Support Router
"""
from fastapi import APIRouter

router = APIRouter(prefix="/support", tags=["support"])


@router.get("/")
async def get_support_tickets():
    """Get support tickets"""
    return {"data": []}


@router.post("/")
async def create_support_ticket():
    """Create support ticket"""
    return {"id": "ticket_123"}
