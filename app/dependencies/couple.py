from fastapi import Depends, HTTPException
from sqlalchemy import select, or_

from app.db.session import AsyncSession, get_async_session
from app.auth.dependencies import get_current_user

from app.models.couple import Couple

async def get_current_couple(
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Couple).where(
            or_(
                Couple.partnerOne_id == user["$id"],
                Couple.partnerTwo_id == user["$id"],
            )
        )
    )

    couple = result.scalar_one_or_none()

    if couple is None:
        raise HTTPException(403, "User not part of couple")

    return couple