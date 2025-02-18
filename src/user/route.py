from fastapi import HTTPException, APIRouter, File, Depends, UploadFile
from fastapi.responses import FileResponse
from .service import user_service
from .model import UserBase, UserRead, UserMe
from utils.token import validate_user_token
from crypto.utils import CryptoUtils
from bson import ObjectId
import aiofiles
import tempfile
import zipfile

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(validate_user_token)],
)



@router.get("/get_user/", response_model=UserRead)
async def get_user(username: str):
    user = await user_service.get_user(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found.")

@router.get("/get_user_od/", response_model=UserBase)
async def get_user_od(user_id: str):
    user = await user_service.get_user_by_objid(user_id)
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

@router.get("/me/", response_model=UserBase)
async def get_me(token: str = Depends(validate_user_token)):
    user_id = token.get("sub") 
    user = await user_service.get_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/generate_key/")
async def generate_rsa_key():
    keys = CryptoUtils.generate_rsa_keys()

    private_key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    public_key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")

    async with aiofiles.open(private_key_file.name, 'w') as private_file:
        await private_file.write(keys['private_key'])

    async with aiofiles.open(public_key_file.name, 'w') as public_file:
        await public_file.write(keys['public_key'])

    zip_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(zip_file.name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(private_key_file.name, "private_key.pem")
        zipf.write(public_key_file.name, "public_key.pem")

    return FileResponse(zip_file.name, filename="rsa_keys.zip")

@router.put("/deactivate/")
async def deactivate_user(user_id: str, option: bool):
    result = await user_service.deactivate(user_id, option)
    if result:
        return {"message": "Account Deactivated"}
    raise HTTPException(status_code=404, detail="User Not Found")

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

@router.put("/is_private/")
async def update_privacy(user_id: str, option: bool):
    modified = await user_service.update_is_private(user_id, option = option)
    try:
        if modified:
         return {"message": "Privacy Updated"}
    except Exception as e:
        print(status_code=404, detail=(e))






