# backend/app/models/support_model.py

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class SupportCaseModel:
    collection_name = "support_cases"

    @staticmethod
    def collection(db):
        return db[SupportCaseModel.collection_name]

    @staticmethod
    async def create_case(db, user_id, subject, description,
                          related_order_id=None):
        case = {
            "user_id": ObjectId(user_id),
            "subject": subject,
            "description": description,
            "related_order_id": ObjectId(related_order_id) if related_order_id else None,
            "status": "open",  # open | in_progress | resolved | closed
            "resolution_notes": None,
            "assigned_to": None,
            "created_at": datetime.utcnow()
        }
        result = await SupportCaseModel.collection(db).insert_one(case)
        case["_id"] = result.inserted_id
        return case

    @staticmethod
    async def update_status(db, case_id, status, resolution_notes=None):
        update = {"status": status}
        if resolution_notes:
            update["resolution_notes"] = resolution_notes

        await SupportCaseModel.collection(db).update_one(
            {"_id": ObjectId(case_id)},
            {"$set": update}
        )