from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pet_state import PetStageEnum
from app.models.couple import Couple

from app.schemas.pet import PetList, PetCreate, PetCreateResponse, PetStateBase, PetStateResponse
from app.schemas.action import PetActionRequest
from app.db.session import get_async_session
from app.dependencies.couple import get_current_couple
from app.auth.dependencies import get_current_user
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
    db: AsyncSession = Depends(get_async_session),
):
    """Returns the current state of the pet."""
    service = PetService(db)

    state = await service.get_pet_state(
        uuid.UUID(pet_id),
        couple.id
    )

    if not state:
        raise HTTPException(status_code=404, detail="Pet not found")

    return PetStateResponse(
        pet_id=state.pet_id,
        name=state.pet.name,
        stage=state.stage,
        xp=state.xp,
        health=state.health,
        happiness=state.happiness,
        energy=state.energy,
        growth_level=state.growth_level,
        mood=state.mood,
        version=state.version,
        last_interaction_at=state.last_interaction_at,
        updated_at=state.updated_at
    )
    
# POST /pets/{pet_id}/state - partners complete a activity/action
@router.post("/{pet_id}/action")
async def perform_pet_action(
    pet_id: str,
    payload: PetActionRequest,
    user=Depends(get_current_user),
    couple: Couple = Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session)
):
    pet_uuid = uuid.UUID(pet_id)

    # Ensure pet belongs to couple
    pet = await PetRepository(db).get_by_id_and_couple(pet_uuid, couple.id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    if pet.state.stage == PetStageEnum.EGG:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Pet must hatch before performing any activities")
    
    service = PetService(db)
    result = await service.process_action(
        pet_id=pet_uuid,
        activity_type=payload.activity_type,
        activity_id=payload.activity_id,
        partner_id=user["$id"],
        idempotency_key=payload.event_id,
    )
    return result