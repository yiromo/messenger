from fastapi import HTTPException, APIRouter

router = APIRouter(
    prefix="/user",
    tags=["User"]
)
