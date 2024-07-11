from fastapi import HTTPException, APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)
