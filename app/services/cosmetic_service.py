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
    
    async def unlock_stage_rewards(self, pet):
        """Unlock cosmetics for the pet’s current stage and auto-equip default ones."""
        stage_cosmetics = await self.repo.get_stage_cosmetics(pet.state.stage)

        equipped_ids = {c.cosmetic_id for c in await self.repo.get_equipped(pet.id)}

        for cosmetic in stage_cosmetics:
            unlock = await self.repo.unlock(pet.id, cosmetic.id, source="growth")
            # auto-equip if nothing of that type is equipped yet
            if unlock and cosmetic.id not in equipped_ids:
                await self.repo.equip(pet.id, cosmetic.id)
    
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

        # Unequip only the same cosmetic type
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.equipped == True,
                PetCosmeticUnlock.cosmetic.has(PetCosmeticUnlock.cosmetic.type == cosmetic_type)
            )
            .values(equipped=False)
        )

        # Equip new one
        await self.db.execute(
            update(PetCosmeticUnlock)
            .where(
                PetCosmeticUnlock.pet_id == pet_id,
                PetCosmeticUnlock.cosmetic_id == cosmetic_id
            )
            .values(equipped=True)
        )

        await self.db.flush()

        return {
            "status": "equipped",
            "equipped": await self.repo.get_equipped(pet_id)
        }