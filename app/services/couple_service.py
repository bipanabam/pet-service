from app.models.couple import Couple
from app.schemas.couple import CoupleBase
from app.services.appwrite_service import get_active_pair

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class CoupleService:
    @staticmethod
    async def get_couple_by_pair_id(pair_id: str, session: AsyncSession):
        result = await session.execute(
            select(Couple).where(Couple.pair_id == pair_id)
        )
        couple = result.scalars().first()

        if not couple:
            raise HTTPException(404, "Couple not found.")

        return couple
    
    @staticmethod
    async def get_or_create_couple(pair_id: str, session: AsyncSession):

        result = await session.execute(
            select(Couple).where(Couple.pair_id == pair_id)
        )
        couple = result.scalars().first()

        if couple:
            return couple

        pair_doc = get_active_pair(pair_id)
        if not pair_doc:
            raise HTTPException(404, "Couple Id Invalid.")

        new_couple = Couple(
            pair_id=pair_doc["$id"],
            partnerOne_id=pair_doc["partnerOne"],
            partnerTwo_id=pair_doc["partnerTwo"]
        )

        session.add(new_couple)
        await session.commit()
        await session.refresh(new_couple)

        return new_couple