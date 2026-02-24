# backend/app/services/event_service.py

from fastapi import HTTPException, status
from bson import ObjectId
from app.models.event_model import EventModel
from app.schemas.event_schema import EventCreate, EventUpdate
from datetime import datetime


class EventService:

    # -----------------------------
    # Create Event (Organizer Only)
    # -----------------------------
    @staticmethod
    async def create_event(event_data: EventCreate, organizer_id: str):

        event_dict = event_data.model_dump()
        event_dict["organizer_id"] = organizer_id

        event_id = await EventModel.create_event(event_dict)

        return {
            "message": "Event created successfully",
            "event_id": event_id
        }

    # -----------------------------
    # Get Single Event
    # -----------------------------
    @staticmethod
    async def get_event(event_id: str):

        event = await EventModel.get_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return EventService._format_event(event)

    # -----------------------------
    # Get All Events
    # -----------------------------
    @staticmethod
    async def get_all_events():

        events = await EventModel.get_all()

        return [EventService._format_event(event) for event in events]

    # -----------------------------
    # Get Organizer Events
    # -----------------------------
    @staticmethod
    async def get_organizer_events(organizer_id: str):

        events = await EventModel.get_by_organizer(organizer_id)

        return [EventService._format_event(event) for event in events]

    # -----------------------------
    # Update Event (Owner Only)
    # -----------------------------
    @staticmethod
    async def update_event(event_id: str, update_data: EventUpdate, current_user: dict):

        event = await EventModel.get_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # Only organizer can update
        if event["organizer_id"] != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this event"
            )

        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}

        await EventModel.update_event(event_id, update_dict)

        return {"message": "Event updated successfully"}

    # -----------------------------
    # Delete Event (Owner Only)
    # -----------------------------
    @staticmethod
    async def delete_event(event_id: str, current_user: dict):

        event = await EventModel.get_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        if event["organizer_id"] != str(current_user["_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this event"
            )

        await EventModel.delete_event(event_id)

        return {"message": "Event deleted successfully"}

    # -----------------------------
    # Format MongoDB Response
    # -----------------------------
    @staticmethod
    def _format_event(event: dict):

        return {
            "id": str(event["_id"]),
            "title": event["title"],
            "description": event["description"],
            "category": event["category"],
            "venue_id": event["venue_id"],
            "organizer_id": event["organizer_id"],
            "event_date": event["event_date"],
            "ticket_price": event["ticket_price"],
            "total_seats": event["total_seats"],
            "tickets_sold": event.get("tickets_sold", 0),
            "status": event.get("status", "upcoming"),
            "created_at": event["created_at"],
            "updated_at": event["updated_at"],
        }