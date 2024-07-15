from postgre import pg

class DBManage:
    async def drop_table(self, table_name: str):
        return await pg.drop_table(table_name)
        
db_manage = DBManage()
