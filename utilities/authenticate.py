from fastapi import HTTPException, Header, status
import os
from config import get_settings

async def verify_token(x_token: str = Header(...)):
    settings = get_settings()
    if x_token != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )