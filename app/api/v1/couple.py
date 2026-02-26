from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.couple import Couple
from app.schemas.couple_schema import CoupleBase
from app.db.session import get_session
from app.services.appwrite_service import get_active_pair, get_user_document
from app.auth.dependencies import get_current_user

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

    couple = session.execute(
        select(Couple)
        .where(Couple.pair_id == pair_id)
    ).first()

    if couple:
        return CoupleBase(
            id=couple[0].id,
            pair_id=couple[0].pair_id,
            partnerOne_id=couple[0].partnerOne_id,
            partnerTwo_id=couple[0].partnerTwo_id,
        )

    pair_doc = get_active_pair(pair_id)
    if not pair_doc:
        raise HTTPException(404, "Pair not active")

    new_couple = Couple(
        pair_id=pair_doc["$id"],
        partnerOne_id=pair_doc["partnerOne"],
        partnerTwo_id=pair_doc["partnerTwo"],
    )

    session.add(new_couple)
    session.commit()
    session.refresh(new_couple)

    return new_couple

@router.get("/{pair_id}", response_model=CoupleBase)
def get_couple(pair_id: str, session: Session = Depends(get_session)):
    couple = session.query(Couple).filter(Couple.pair_id == pair_id).first()
    if not couple:
        raise HTTPException(status_code=404, detail="Couple data not found in local database. Please sync first.")
    return couple