from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.pet_cosmetic import PetCosmetic, PetCosmeticUnlock

class CosmeticRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_catalog(self):
        result = await self.db.execute(select(PetCosmetic))
        return result.scalars().all()

    async def get_pet_inventory(self, pet_id):
        result = await self.db.execute(
            select(PetCosmeticUnlock)
            .where(PetCosmeticUnlock.pet_id == pet_id)
            .options(selectinload(PetCosmeticUnlock.cosmetic))
        )
        return result.scalars().all()

    async def get_equipped(self, pet_id):
        result = await self.db.execute(
            select(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.equipped == True
            )
            .options(selectinload(PetCosmeticUnlock.cosmetic))
        )
        return result.scalars().all()

    async def unlock(self, pet_id, cosmetic_id, source):
        unlock = PetCosmeticUnlock(
            pet_id=pet_id,
            cosmetic_id=cosmetic_id,
            unlock_source=source
        )
        self.db.add(unlock)
        await self.db.flush()
        return unlock