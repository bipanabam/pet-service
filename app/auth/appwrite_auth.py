from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import httpx

from app.core.config import config

security = HTTPBearer()

APPWRITE_ENDPOINT = config.APPWRITE_ENDPOINT
PROJECT_ID = config.APPWRITE_PROJECT_ID


async def appwrite_auth(token=Depends(security)):
    jwt = token.credentials

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{APPWRITE_ENDPOINT}/account",
            headers={
                "X-Appwrite-Project": PROJECT_ID,
                "Authorization": f"Bearer {jwt}",
            },
        )

    if res.status_code != 200:
        raise HTTPException(401, "Invalid JWT")

    return res.json()