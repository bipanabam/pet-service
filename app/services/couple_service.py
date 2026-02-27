from app.models.couple import Couple
from app.schemas.couple import CoupleBase
from app.services.appwrite_service import get_active_pair

from fastapi import HTTPException
from sqlalchemy import select

class CoupleService:
    @staticmethod
    def get_couple_by_pair_id(pair_id: str, session):
        couple = session.query(Couple).filter(Couple.pair_id == pair_id).first()
        if not couple:
            raise HTTPException(status_code=404, detail="Couple not found. Please sync first.")
        return couple
    
    @staticmethod
    def get_or_create_couple(pair_id: str, session):
        couple = session.execute(
            select(Couple)
            .where(Couple.pair_id == pair_id)
        ).scalars().first()
        
        if couple:
            return CoupleBase(
                id=couple.id,
                pair_id=couple.pair_id,
                partnerOne_id=couple.partnerOne_id,
                partnerTwo_id=couple.partnerTwo_id
            )
        
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