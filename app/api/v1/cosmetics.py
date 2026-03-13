from fastapi import APIRouter, Depends, HTTPException
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