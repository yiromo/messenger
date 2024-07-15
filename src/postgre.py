import asyncpg 
from config import settings

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=settings.POSTGRES_URL)

    async def close(self):
        await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def insert_one(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(f'${i+1}' for i in range(len(data)))
        query = f'INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *'
        return await self.fetchrow(query, *data.values())

    async def find_one(self, table, criteria):
        condition = ' AND '.join(f"{key} = ${i+1}" for i, key in enumerate(criteria.keys()))
        query = f'SELECT * FROM {table} WHERE {condition} LIMIT 1'
        return await self.fetchrow(query, *criteria.values())

    async def find(self, table, criteria):
        condition = ' AND '.join(f"{key} = ${i+1}" for i, key in enumerate(criteria.keys()))
        query = f'SELECT * FROM {table} WHERE {condition}'
        return await self.fetch(query, *criteria.values())

    async def update_one(self, table, criteria, new_data):
        set_clause = ', '.join(f"{key} = ${i+1}" for i, key in enumerate(new_data.keys()))
        condition = ' AND '.join(f"{key} = ${len(new_data)+i+1}" for i, key in enumerate(criteria.keys()))
        query = f'UPDATE {table} SET {set_clause} WHERE {condition} RETURNING *'
        return await self.fetchrow(query, *new_data.values(), *criteria.values())

    async def delete_one(self, table, criteria):
        condition = ' AND '.join(f"{key} = ${i+1}" for i, key in enumerate(criteria.keys()))
        query = f'DELETE FROM {table} WHERE {condition} RETURNING *'
        return await self.fetchrow(query, *criteria.values())

    async def delete_many(self, table, criteria):
        condition = ' AND '.join(f"{key} = ${i+1}" for i, key in enumerate(criteria.keys()))
        query = f'DELETE FROM {table} WHERE {condition}'
        return await self.execute(query, *criteria.values())

    async def drop_table(self, table):
        query = f'DROP TABLE IF EXISTS {table} CASCADE'
        return await self.execute(query)
    
    async def create_table_if_not_exists(self, table_name, fields):
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(fields)}
            )
        '''
        await self.execute(query)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance


pg = Database()