# backend/app/models/user_model.py

from datetime import datetime
from bson import ObjectId
<<<<<<< HEAD
from app.db import db
from app.core.roles import UserRole
=======
from motor.motor_asyncio import AsyncIOMotorDatabase
>>>>>>> 90311fb5e67d0399c89df62fdb9cba6ef34480da


class UserModel:
    collection_name = "users"

    @staticmethod
    def collection(db: AsyncIOMotorDatabase):
        return db[UserModel.collection_name]

    @staticmethod
    async def create_user(db, name, email, hashed_password, role):
        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,  # admin | organizer | customer | entry_manager | support
            "created_at": datetime.utcnow()
        }
        result = await UserModel.collection(db).insert_one(user)
        user["_id"] = result.inserted_id
        return user

    @staticmethod
    async def get_by_email(db, email):
        return await UserModel.collection(db).find_one({"email": email})

    @staticmethod
    async def get_by_id(db, user_id):
        return await UserModel.collection(db).find_one({"_id": ObjectId(user_id)})