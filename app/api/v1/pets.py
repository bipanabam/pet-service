from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.models.pet import Pet
from app.models.couple import Couple
from app.schemas.pet_schema import PetList
from app.db.session import get_session
from app.dependencies.couple import get_current_couple

router = APIRouter(
    prefix="/pets", 
    tags=["pets"]
    )

# GET /pets - Get all pets
@router.get("/", response_model=PetList)
def get_pets(
    couple: Couple = Depends(get_current_couple),
    session: Session = Depends(get_session),
):
    
    if not couple:
        raise HTTPException(status_code=403, detail="User not part of couple")
    
    pets = (
        session.query(Pet)
        .filter(Pet.couple_id == couple.id)
        .all()
    )
    if not pets:
        raise HTTPException(status_code=404, detail="No pets raised yet.")
    return PetList(
        results=pets,
        count=len(pets),
    )