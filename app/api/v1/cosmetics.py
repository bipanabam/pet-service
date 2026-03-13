from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.session import get_async_session
from app.services.cosmetic_service import CosmeticService
from app.dependencies.couple import get_current_couple

from app.repositories.pet_repository import PetRepository
from app.schemas.cosmetic import PetCosmeticCatalog

router = APIRouter(
    prefix="/cosmetics",
    tags=["cosmetics"]
)

@router.get("/", response_model=PetCosmeticCatalog)
async def get_cosmetics(
    db: AsyncSession = Depends(get_async_session)
):
    """Returns all pet cosmetics available in our digital pet system"""
    service = CosmeticService(db)
    all_catalog =  await service.get_catalog()
    return PetCosmeticCatalog(
        results=all_catalog,
        count=len(all_catalog)
    )
    
@router.get("/pets/{pet_id}")
async def get_pet_cosmetics(
    pet_id: uuid.UUID,
    couple=Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session)
):
    pet = await PetRepository(db).get_by_id_and_couple(pet_id, couple.id)

    if not pet:
        raise HTTPException(404, "Pet not found")

    service = CosmeticService(db)
    await service.unlock_stage_rewards(pet)
    pet_inventory =  await service.get_pet_inventory(pet_id)
    
    if not pet_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found in the inventory")
    return pet_inventory
    
@router.post("/pets/{pet_id}/equip/{cosmetic_id}")
async def equip_cosmetic(
    pet_id: uuid.UUID,
    cosmetic_id: str,
    couple=Depends(get_current_couple),
    db: AsyncSession = Depends(get_async_session)
):

    pet = await PetRepository(db).get_by_id_and_couple(pet_id, couple.id)

    if not pet:
        raise HTTPException(404, "Pet not found")

    service = CosmeticService(db)

    try:
        return await service.equip_cosmetic(
            pet_id,
            uuid.UUID(cosmetic_id)
        )
    except ValueError as e:
        raise HTTPException(400, str(e))