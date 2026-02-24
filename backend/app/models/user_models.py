# backend/app/models/user_model.py

from datetime import datetime
from bson import ObjectId
from typing import Optional

from app.db import get_database


class UserModel:
    collection_name = "users"

    @staticmethod
    def collection(db=None):
        db = db if db is not None else get_database()
        return db[UserModel.collection_name]

    @staticmethod
    async def create_user(user_data: dict, db=None):
        db = db if db is not None else get_database()
        user = {
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "password": user_data.get("password"),
            "role": user_data.get("role", "customer"),
            "is_active": user_data.get("is_active", True),
            "created_at": datetime.utcnow(),
        }
        db = db if db is not None else get_database()
        result = await UserModel.collection(db).insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_email(email: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        return await UserModel.collection(db).find_one({"email": email})

    @staticmethod
    async def get_by_id(user_id: str, db=None) -> Optional[dict]:
        db = db if db is not None else get_database()
        return await UserModel.collection(db).find_one({"_id": ObjectId(user_id)})