from fastapi import HTTPException, APIRouter, WebSocket, UploadFile, File
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from .websocket import chat_ws_handler
from .service import chat_service, init
from postgre import pg
from crypto.utils import CryptoUtils
from .model import ChatLineResponse, ChatLine
from typing import List

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/create/")
async def create_chat():
    chat = await chat_service.create_chat()
    return {"chat_uuid": chat.id}

@router.post("/create_user/")
async def add_user(obj_id: str):
    user = await chat_service.add_user(obj_id)
    return {"user_pg_id": user.id}

@router.post("/chat_history/", response_model=List[ChatLineResponse])
async def chat_history(chat_id: str, recipient_private_key: UploadFile = File(...)):
    try:
        key_data = await recipient_private_key.read()
        recipient_private_key = CryptoUtils.load_private_key(key_data.decode('utf-8'))
        chat_lines = await chat_service.get_chat_lines(chat_id, recipient_private_key)
        return chat_lines
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error decrypting messages: {str(e)}")


@router.post("/{chat_id}/add_user/{user_id}/")
async def add_user_to_chat(chat_id: str, user_id: str):
    chat_user = await chat_service.add_user_to_chat(chat_id, user_id)
    if not chat_user:
        raise HTTPException(status_code=404, detail="Chat or user not found")
    return JSONResponse(content={"message": "User added to chat successfully"})

@router.post("/{chat_id}/send_message/{user_id}/")
async def send_message(chat_id: str, user_id: str, message: str, recipient_public_key: UploadFile = File(...)):
    try:
        public_key_str = await recipient_public_key.read()
        public_key = CryptoUtils.load_public_key(public_key_str.decode('utf-8'))
        chat_line = await chat_service.send_message(chat_id, user_id, message, public_key)
        if not chat_line:
            raise HTTPException(status_code=404, detail="Chat or user not found")
        return JSONResponse(content={"message": "Message sent successfully"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid public key: {str(e)}")

@router.put("/{chat_id}/update/{message_id}")
async def update_message(chat_id: str, message_id: int, text: str):
    updated_line = await chat_service.update_message(chat_id, message_id, text)
    if not updated_line:
        raise HTTPException(status_code=404, detail="Error updating message")
    return {"true"}

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


