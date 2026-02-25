from fastapi import APIRouter, HTTPException, Depends, Response
from sqlmodel import Session

from app.models.couple import Couple
from app.schemas.couple_schema import CoupleSync, CoupleBase
from app.db.session import get_session
from app.services.appwrite_service import get_pair

router = APIRouter(
    prefix="/couple",
    tags=["couple"]
)

@router.post("/sync", response_model=CoupleBase)
def sync_couple(payload: CoupleSync, session: Session = Depends(get_session)):
    pair_id = payload.pair_id
    if not pair_id:
        raise HTTPException(status_code=400, detail="pair_id is required")
    
    data = session.query(Couple).filter(Couple.id == payload.pair_id).first()
    if data:
        return Response(status_code=204, content="Already synced with Appwrite")  # No content, already exists
    
    # check if given pair id exists in appwrite, 
    pair_doc = get_pair(payload.pair_id)
    if not pair_doc:
        raise HTTPException(status_code=404, detail="Pair not found in Appwrite")
    
    try:
        new_couple = Couple(
            id=pair_doc["$id"],
            partnerOne_id=pair_doc["partnerOne"],
            partnerTwo_id=pair_doc["partnerTwo"]
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in Appwrite response: {e}")
    session.add(new_couple)
    session.commit()
    session.refresh(new_couple)
    return new_couple