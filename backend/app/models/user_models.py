# backend/app/models/user_model.py

from datetime import datetime
from bson import ObjectId
from app.db import db
from app.core.roles import UserRole


class UserModel:
    collection = db["users"]

    @staticmethod
    async def create_user(user_data: dict):
        user_data["role"] = user_data.get("role", UserRole.CUSTOMER)
        user_data["is_active"] = True
        user_data["is_verified"] = False
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()

        result = await UserModel.collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_email(email: str):
        return await UserModel.collection.find_one({"email": email})

    @staticmethod
    async def get_by_id(user_id: str):
        return await UserModel.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def update_user(user_id: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow()
        return await UserModel.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

    @staticmethod
    async def delete_user(user_id: str):
        return await UserModel.collection.delete_one({"_id": ObjectId(user_id)})