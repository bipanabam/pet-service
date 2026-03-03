from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pet import Pet
from app.models.pet_state import PetState
from app.models.couple import Couple

from app.schemas.pet import PetList, PetCreate, PetCreateResponse, PetStateBase, PetStateResponse
from app.schemas.action import PetActionRequest
from app.db.session import get_async_session
from app.dependencies.couple import get_current_couple
from app.services.pet_service import PetService
from app.repositories.pet_repository import PetRepository

import uuid

router = APIRouter(
    prefix="/pets", 
    tags=["pets"]
    )

# GET /pets - Get all pets
@router.get("/", response_model=PetList)
async def get_pets(
    couple: Couple = Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session),
):
    """Returns all pets owned by authenticated couple."""
    pets = await PetRepository(db).get_by_couple(couple.id)
    
    if not pets:
        raise HTTPException(status_code=404, detail="No pet started raising yet.")
    return PetList(
        results=pets,
        count=len(pets),
    )
    
# POST /pets - Create a new pet
@router.post("/", response_model=PetCreateResponse)
async def create_pet(
    payload: PetCreate,
    couple: Couple = Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session),
):
    service = PetService(db)

    try:
        new_pet = await service.create_pet(couple.id, payload)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return new_pet
    
    
# GET /pets/{pet_id}/state - Get pet state
@router.get("/{pet_id}/state", response_model=PetStateResponse)
async def get_pet_state(
    pet_id: str,
    couple: Couple = Depends(get_current_couple),
    session: AsyncSession = Depends(get_async_session),
):
    """Returns the current state of the pet."""
    pet = await PetRepository(session).get_by_id_and_couple(uuid.UUID(pet_id), couple.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    result = await session.execute(
        select(PetState).where(
            PetState.pet_id == uuid.UUID(pet_id)
        )
    )
    
    pet_state = result.scalar_one_or_none()
    
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
    
# POST /pets/{pet_id}/state - partners complete a activity/action
@router.post("/{pet_id}/action")
async def perform_pet_action(
    pet_id: str,
    payload: PetActionRequest,
    couple: Couple = Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session)
):
    # Ensure pet belongs to couple
    pet = await PetRepository(db).get_by_id_and_couple(uuid.UUID(pet_id), couple.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = await PetService.process_action(
        db=db,
        pet_id=pet_id,
        activity_type=payload.activity_type,
        activity_id=payload.activity_id,
        idempotency_key=payload.event_id
    )
    return result