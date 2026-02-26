from fastapi import APIRouter, HTTPException, Depends,status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.pet import Pet
from app.models.pet_state import PetState
from app.models.couple import Couple
from app.schemas.pet_schema import PetList, PetCreate, PetCreateResponse, PetStateBase
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
    
    pets = session.execute(
        select(Pet)
        .options(selectinload(Pet.state))
        .where(Pet.couple_id == couple.id)
    ).scalars().all()
    
    if not pets:
        raise HTTPException(status_code=404, detail="No pet started raising yet.")
    return PetList(
        results=pets,
        count=len(pets),
    )
    
# POST /pets - Create a new pet
@router.post("/", response_model=PetCreateResponse)
def create_pet(
    payload: PetCreate,
    couple: Couple = Depends(get_current_couple),
    session: Session = Depends(get_session),
):
    if not couple:
        raise HTTPException(status_code=403, detail="User not part of a couple")
    
    try:
        new_pet = Pet(
            name=payload.name,
            pet_type=payload.pet_type,
            couple_id=couple.id,
        )
        session.add(new_pet)
        session.flush()  # assigns ID without committing

        pet_state = PetState(
            pet_id=new_pet.id,
            stage="egg",
            xp=0,
            growth_level=1,
            health=100,
            happiness=100,
            energy=100,
            version=1,
        )
        session.add(pet_state)
        session.commit()
        session.refresh(new_pet)
        session.refresh(pet_state)   
        
        return new_pet
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create pet: {str(e)}")