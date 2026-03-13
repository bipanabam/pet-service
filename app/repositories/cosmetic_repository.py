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
    
    async def get_stage_cosmetics(self, stage):
        """Fetch cosmetics unlockable at this stage."""
        result = await self.db.execute(
            select(PetCosmetic).where(PetCosmetic.required_stage == stage)
        )
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
        """Unlock a cosmetic for a pet, idempotent."""
        existing = await self.db.execute(
            select(PetCosmeticUnlock).where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.cosmetic_id == cosmetic_id
            )
        )
        if existing.scalar_one_or_none():
            return None  # already unlocked

        unlock = PetCosmeticUnlock(
            pet_id=pet_id,
            cosmetic_id=cosmetic_id,
            unlock_source=source
        )
        self.db.add(unlock)
        await self.db.flush()
        return unlock
    
    async def equip(self, pet_id, cosmetic_id):
        """Equip cosmetic, unequipping same type."""
        # fetch inventory
        inventory = await self.get_pet_inventory(pet_id)
        cosmetic = next((i for i in inventory if i.cosmetic_id == cosmetic_id), None)
        if not cosmetic:
            raise ValueError("Cosmetic not owned")

        cosmetic_type = cosmetic.cosmetic.type

        # unequip same type
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.equipped == True,
                PetCosmeticUnlock.cosmetic.has(PetCosmetic.type == cosmetic_type)
            )
            .values(equipped=False)
        )

        # equip new
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.cosmetic_id == cosmetic_id
            )
            .values(equipped=True)
        )
        await self.db.flush()