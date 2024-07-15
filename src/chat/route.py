from fastapi import HTTPException, APIRouter, WebSocket
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from .websocket import chat_ws_handler
from .service import chat_service, init
from postgre import pg


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/create/")
async def create_chat():
    chat = await chat_service.create_chat()
    return {"chat_uuid": chat.id}

@router.post("/{chat_id}/add_user/{user_id}/")
async def add_user_to_chat(chat_id: str, user_id: str):
    chat_user = await chat_service.add_user_to_chat(chat_id, user_id)
    if not chat_user:
        raise HTTPException(status_code=404, detail="Chat or user not found")
    return JSONResponse(content={"message": "User added to chat successfully"})

@router.post("/{chat_id}/send_message/{user_id}/")
async def send_message(chat_id: str, user_id: str, message: str):
    chat_line = await chat_service.send_message(chat_id, user_id, message)
    if not chat_line:
        raise HTTPException(status_code=404, detail="Chat or user not found")
    return JSONResponse(content={"message": "Message sent successfully"})

@router.websocket_route("/{chat_id}/ws")
async def websocket_endpoint(chat_id: int, websocket: WebSocket):
    await chat_ws_handler(websocket, chat_id)

@router.on_event("startup")
async def startup():
    await pg.connect()
    await init()

@router.on_event("shutdown")
async def shutdown():
    await pg.close()