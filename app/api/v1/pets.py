from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.pet import Pet
from app.models.pet_state import PetState
from app.models.couple import Couple
from app.schemas.pet import PetList, PetCreate, PetCreateResponse, PetStateBase, PetStateResponse
from app.db.session import get_session
from app.dependencies.couple import get_current_couple
from app.services.pet_service import PetService

import uuid

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
    """Returns all pets owned by authenticated couple."""
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
    db: Session = Depends(get_session),
):
    service = PetService(db)
    try:
        new_pet = service.create_pet(couple.id, payload)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return new_pet
    
    
# GET /pets/{pet_id}/state - Get pet state
@router.get("/{pet_id}/state", response_model=PetStateResponse)
def get_pet_state(
    pet_id: str,
    couple: Couple = Depends(get_current_couple),
    session: Session = Depends(get_session),
):
    """Returns the current state of the pet."""
    pet_state = session.execute(
        select(PetState)
        .where(PetState.pet_id == uuid.UUID(pet_id))
    ).scalar_one_or_none()

    if not pet_state:
        raise HTTPException(status_code=404, detail="Pet state not found")

    return PetStateResponse(
        pet_id=pet_state.pet_id,
        name=pet_state.pet.name,
        stage=pet_state.stage,
        xp=pet_state.xp,
        health=pet_state.health,
        happiness=pet_state.happiness,
        energy=pet_state.energy,
        growth_level=pet_state.growth_level,
        mood=pet_state.mood,
        version=pet_state.version,
        last_interaction_at=pet_state.last_interaction_at,
        updated_at=pet_state.updated_at
    )
 