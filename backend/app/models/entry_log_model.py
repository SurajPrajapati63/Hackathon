from datetime import datetime
from bson import ObjectId


def entry_log_entity(entry) -> dict:
    return {
        "id": str(entry["_id"]),
        "ticket_id": str(entry["ticket_id"]),
        "event_id": str(entry["event_id"]),
        "validated_by": str(entry["validated_by"]),
        "validation_status": entry["validation_status"],
        "entry_time": entry["entry_time"],
    }


def entry_log_model(
    ticket_id: ObjectId,
    event_id: ObjectId,
    validated_by: ObjectId,
    validation_status: str,
):
    return {
        "ticket_id": ticket_id,
        "event_id": event_id,
        "validated_by": validated_by,  # entry manager ID
        "validation_status": validation_status,  # success | failed
        "entry_time": datetime.utcnow(),
    }