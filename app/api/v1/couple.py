from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.couple import Couple
from app.schemas.couple import CoupleBase
from app.db.session import get_async_session
from app.services.appwrite_service import get_active_pair, get_user_document
from app.auth.dependencies import get_current_user
from app.services.couple_service import CoupleService

router = APIRouter(
    prefix="/couple",
    tags=["couple"]
)

@router.post("/sync", response_model=CoupleBase)
async def sync_couple(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_doc = get_user_document(user["$id"])
    pair_id = user_doc.get("pairId")

    if not pair_id:
        raise HTTPException(403, "User not paired yet.")

    couple = await CoupleService.get_or_create_couple(pair_id, session)
    return couple

@router.get("/{pair_id}", response_model=CoupleBase)
async def get_couple(pair_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        couple = await CoupleService.get_couple_by_pair_id(pair_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=f"{e.detail}")
    return couple