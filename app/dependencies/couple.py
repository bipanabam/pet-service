from fastapi import Depends, HTTPException
from app.auth.dependencies import get_current_user

from app.models.couple import Couple
from app.db.session import Session, get_session

async def get_current_couple(
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    couple = (
        session.query(Couple)
        .filter((Couple.partnerOne_id == user["$id"]) | (Couple.partnerTwo_id == user["$id"]))
        .first()
    )

    if not couple:
        raise HTTPException(403, "User not part of couple")

    return couple