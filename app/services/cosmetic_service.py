from sqlalchemy import update
from app.repositories.cosmetic_repository import CosmeticRepository
from app.models.pet_cosmetic import PetCosmeticUnlock


class CosmeticService:

    def __init__(self, db):
        self.db = db
        self.repo = CosmeticRepository(db)

    async def get_catalog(self):
        return await self.repo.get_catalog()

    async def get_pet_inventory(self, pet_id):
        return await self.repo.get_pet_inventory(pet_id)

    async def equip_cosmetic(self, pet_id, cosmetic_id):

        inventory = await self.repo.get_pet_inventory(pet_id)

        cosmetic = None
        for item in inventory:
            if item.cosmetic_id == cosmetic_id:
                cosmetic = item
                break

        if not cosmetic:
            raise ValueError("Cosmetic not owned")

        cosmetic_type = cosmetic.cosmetic.type

        # unequip same type
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.equipped == True
            )
            .values(equipped=False)
        )

        # equip new one
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.cosmetic_id == cosmetic_id
            )
            .values(equipped=True)
        )

        await self.db.flush()

        return {"status": "equipped"}