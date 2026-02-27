from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.couple import Couple
from app.schemas.couple import CoupleBase
from app.db.session import get_session
from app.services.appwrite_service import get_active_pair, get_user_document
from app.auth.dependencies import get_current_user
from app.services.couple_service import CoupleService

router = APIRouter(
    prefix="/couple",
    tags=["couple"]
)

@router.post("/sync", response_model=CoupleBase)
def sync_couple(
    user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_doc = get_user_document(user["$id"])
    pair_id = user_doc.get("pairId")

    if not pair_id:
        raise HTTPException(403, "User not paired yet. Please pair first in the app.")

    try:
        couple = CoupleService.get_or_create_couple(pair_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=f"{e.detail}")
    return couple

@router.get("/{pair_id}", response_model=CoupleBase)
def get_couple(pair_id: str, session: Session = Depends(get_session)):
    try:
        couple = CoupleService.get_couple_by_pair_id(pair_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=f"{e.detail}")
    return couple