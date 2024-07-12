from fastapi import HTTPException, APIRouter, File, Depends, UploadFile
from utils.token import validate_token
from .service import user_service
from .model import UserRead

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/get_user/", response_model=UserRead)
async def get_user(username: str):
    user = await user_service.get_user(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found.")

@router.put("/update_username/")
async def update_username(user_id:str, username: str):
    modified = await user_service.update_username(user_id, username)
    if modified:
        return {"message": "Username succesfully updated."}
    raise HTTPException(status_code=404, detail="Error.")

@router.put("/update_email/")
async def update_user_email(user_id: str, email: str):
    modified = await user_service.update_user_add_email(user_id, email)
    if modified:
        return {"message": "User email updated successfully."}
    raise HTTPException(status_code=404, detail="User not found.")

@router.delete("/delete/")
async def delete_user(user_id: str):
    deleted = await user_service.delete_user(user_id)
    if deleted:
        return {"message": "User deleted successfully."}
    raise HTTPException(status_code=404, detail="User not found.")

@router.put("/put_pfp/")
async def update_pfp(user_id: str,file: UploadFile = File(...)):
    modified, file_url = await user_service.update_pfp(user_id, file)
    if modified:
        return {"message":  "Profile picture uploaded", "file_url": file_url}
    raise HTTPException(status_code=404, detail="Error")


