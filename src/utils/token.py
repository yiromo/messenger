from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config import settings


async def create_token(data: dict, token_type: str = "access"):
    to_encode = data.copy()
    expire_time_minutes = (
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
        if token_type == "access"
        else settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    expire = datetime.utcnow() + timedelta(minutes=expire_time_minutes)
    to_encode.update({"exp": expire, "token_type": token_type})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

async def validate_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/admin/login/"))):
    if token == settings.API_TOKEN:
        return {"type": "messenger"}
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=400, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
async def validate_websocket_token(token: str):
    if token == settings.API_TOKEN:
        return {"type": "messenger"}
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("exp") < datetime.utcnow().timestamp():
            return None
        return payload
    except JWTError:
        return None
    
'''async def regenerate_refresh_token(token: str):
    payload = await validate_token(token=token)
    if payload["token_type"] != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    access_token = await create_token(
        data={
            "sub": payload.get("sub"),
            "role": payload.get("role"),
        }
    )
    refresh_token = await create_token(
        data={
            "sub": payload.get("sub"),
            "role": payload.get("role"),
        },
        token_type="refresh",
    )
    return {"accessToken": access_token, "refreshToken": refresh_token}
'''