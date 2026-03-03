from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, UUID
from sqlalchemy.orm import selectinload
from app.models.pet import Pet

class PetRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_couple(self, couple_id: UUID):
        result = await self.db.execute(
            select(Pet)
            .options(selectinload(Pet.state))
            .where(Pet.couple_id == couple_id)
        )
        return result.scalars().all()

    async def count_by_couple(self, couple_id: UUID):
        result = await self.db.execute(
            select(func.count())
            .select_from(Pet)
            .where(Pet.couple_id == couple_id)
        )
        return result.scalar_one()

    async def pet_name_exists(self, couple_id: UUID, pet_name: str):
        result = await self.db.execute(
            select(
                select(Pet)
                .where(
                    Pet.couple_id == couple_id,
                    Pet.name == pet_name
                )
                .exists()
            )
        )
        return result.scalar()
    
    async def get_by_id_and_couple(self, pet_id: UUID, couple_id: UUID):
        result = await self.db.execute(
            select(Pet)
            .where(Pet.id == pet_id, Pet.couple_id == couple_id)
            .options(selectinload(Pet.state))
        )
        return result.scalar_one_or_none()

    async def create(self, *, name, pet_type, couple_id):
        pet = Pet(
            name=name,
            pet_type=pet_type,
            couple_id=couple_id,
        )
        self.db.add(pet)
        await self.db.flush()
        return pet