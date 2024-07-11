from fastapi import HTTPException, APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
