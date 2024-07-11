from fastapi import HTTPException, APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

