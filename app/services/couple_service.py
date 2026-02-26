from app.models.couple import Couple
from app.services.appwrite_service import get_active_pair

from fastapi import HTTPException

def get_or_create_couple(pair_id: str, session):
    couple = session.query(Couple).filter(Couple.pair_id == pair_id).first()
    if couple:
        return couple
    
    pair_doc = get_active_pair(pair_id)
    if not pair_doc:
        raise HTTPException(status_code=404, detail="Couple Id Invalid.")
    
    new_couple = Couple(
        pair_id=pair_doc["$id"],
        partnerOne_id=pair_doc["partnerOne"],
        partnerTwo_id=pair_doc["partnerTwo"]
    )
    session.add(new_couple)
    session.commit()
    session.refresh(new_couple)
    return new_couple