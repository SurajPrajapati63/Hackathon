from datetime import datetime
from bson import ObjectId


def support_case_entity(support) -> dict:
    return {
        "id": str(support["_id"]),
        "user_id": str(support["user_id"]),
        "order_id": str(support.get("order_id")) if support.get("order_id") else None,
        "category": support["category"],
        "description": support["description"],
        "status": support["status"],
        "resolution_notes": support.get("resolution_notes"),
        "created_at": support["created_at"],
        "updated_at": support["updated_at"],
    }


def support_case_model(
    user_id: ObjectId,
    category: str,
    description: str,
    order_id: ObjectId = None,
):
    return {
        "user_id": user_id,
        "order_id": order_id,  # optional
        "category": category,  # refund / technical / other
        "description": description,
        "status": "open",  # open | in_progress | resolved
        "resolution_notes": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }