from pymongo import MongoClient
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

client = AsyncIOMotorClient(DATABASE_URL)
#client.server_info()
#print("Connection to the database established successfully.")
db = client.messenger
coll = db.get_collection("users")
chat_coll = db.get_collection("chats")

