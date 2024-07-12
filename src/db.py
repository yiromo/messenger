from motor import motor_asyncio 
from config import settings

class Database:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
        self.db = self.client[settings.DATABASE_NAME]

    async def insert_one(self, collection, data):
        return await self.db[collection].insert_one(data)

    async def find_one(self, collection, data):
        return await self.db[collection].find_one(data)

    async def find(self, collection, data):
        return await self.db[collection].find(data, {"_id": 0})

    async def update_one(self, collection, data, new_data):
        return await self.db[collection].update_one(data, new_data)

    async def delete_one(self, collection, data):
        return await self.db[collection].delete_one(data)

    async def delete_many(self, collection, data):
        return await self.db[collection].delete_many(data)

    async def drop_collection(self, collection):
        return await self.db[collection].drop()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

db = Database()
