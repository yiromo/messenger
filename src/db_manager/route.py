from .service import db_manage
from fastapi import APIRouter, Depends, HTTPException
from utils.token import validate_token
from user.model import UserBase
from user.service import user_service


router = APIRouter(
    prefix="/db_manage",
    tags=["Database Management"]
)

@router.delete("/drop_table/")
async def drop_table_pg(table: str):
    try:
        result = await db_manage.drop_table(table_name=table)
        return {"detail": f"Table {table} dropped successfully"}
    except Exception as e:
        return {"detail": f"Failed to drop table {table}: {str(e)}"}

@router.get("/get_user_all_info/", response_model=UserBase)
async def get_user_mongo(username: str):
    user = await user_service.get_user_all(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found.")


