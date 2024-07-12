from pymongo.collection import Collection
from db import db
from bson.objectid import ObjectId
from .model import UserRead
from typing import Optional
from utils.bucket import bucket_images
from fastapi import UploadFile

def convert_object_id(doc):
    if "_id" in doc:
        doc["objectId"] = str(doc["_id"])
    if "password" in doc:
        del doc["password"] 
    return doc


class User:
    def __init__(self, collection):
        self.collection: Collection = db.db[collection]

    async def get_user(self, username: str) -> Optional[UserRead]:
        result = await self.collection.find_one({"username": username})
        if result:
            result = convert_object_id(result)
            return UserRead(**result)
        return None
    
    async def update_user_add_email(self, user_id, email):
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"email": email}}
        )
        return result.modified_count
    
    async def update_username(self, user_id, username):
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"username": username}}
        )
        return result.modified_count
    
    async def update_pfp(self, user_id, file: UploadFile):
        file_name = f"{user_id}/{file.filename}"
        file_content = await file.read()
        bucket_images.upload_file(file=file_content, file_name=file_name)
        file_url = bucket_images.get_file_url(file_name)
        result = await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"profile_picture": file_url}})
        return result.modified_count, file_url
    
    async def delete_pfp(self, user_id, file):
        pass

    async def delete_user(self, user_id):
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count
    
user_service = User("users")