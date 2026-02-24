# backend/app/services/venue_service.py

from fastapi import HTTPException, status
from app.models.venue_model import VenueModel
from app.schemas.venue_schema import VenueCreate, VenueUpdate


class VenueService:

    # -----------------------------
    # Create Venue (Admin Only Recommended)
    # -----------------------------
    @staticmethod
    async def create_venue(venue_data: VenueCreate):

        venue_dict = venue_data.model_dump()
        venue_id = await VenueModel.create_venue(venue_dict)

        return {
            "message": "Venue created successfully",
            "venue_id": venue_id
        }

    # -----------------------------
    # Get Single Venue
    # -----------------------------
    @staticmethod
    async def get_venue(venue_id: str):

        venue = await VenueModel.get_by_id(venue_id)

        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

        return VenueService._format_venue(venue)

    # -----------------------------
    # Get All Venues
    # -----------------------------
    @staticmethod
    async def get_all_venues():

        venues = await VenueModel.get_all()

        return [VenueService._format_venue(v) for v in venues]

    # -----------------------------
    # Update Venue
    # -----------------------------
    @staticmethod
    async def update_venue(venue_id: str, update_data: VenueUpdate):

        venue = await VenueModel.get_by_id(venue_id)

        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

        update_dict = {
            k: v for k, v in update_data.model_dump().items() if v is not None
        }

        await VenueModel.update_venue(venue_id, update_dict)

        return {"message": "Venue updated successfully"}

    # -----------------------------
    # Delete Venue
    # -----------------------------
    @staticmethod
    async def delete_venue(venue_id: str):

        venue = await VenueModel.get_by_id(venue_id)

        if not venue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )

        await VenueModel.delete_venue(venue_id)

        return {"message": "Venue deleted successfully"}

    # -----------------------------
    # Format MongoDB Response
    # -----------------------------
    @staticmethod
    def _format_venue(venue: dict):

        return {
            "id": str(venue["_id"]),
            "name": venue["name"],
            "location": venue["location"],
            "capacity": venue["capacity"],
            "description": venue.get("description"),
            "created_at": venue["created_at"],
            "updated_at": venue["updated_at"],
        }