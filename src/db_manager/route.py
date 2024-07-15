from .service import db_manage
from fastapi import APIRouter

router = APIRouter(
    prefix="/db_manage",
    tags=["Database Management"]
)

@router.delete("/drop_table/")
async def drop_table(table: str):
    try:
        result = await db_manage.drop_table(table_name=table)
        return {"detail": f"Table {table} dropped successfully"}
    except Exception as e:
        return {"detail": f"Failed to drop table {table}: {str(e)}"}

