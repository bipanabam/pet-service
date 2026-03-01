from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, UUID, func
from app.models.pet import Pet

class PetRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_couple(self, couple_id: UUID):
        return self.db.execute(
            select(Pet)
            .options(selectinload(Pet.state))
            .where(Pet.couple_id == couple_id)
        ).scalars().all()

    def count_by_couple(self, couple_id: UUID):
        return self.db.scalar(
            select(func.count())
            .select_from(Pet)
            .where(Pet.couple_id == couple_id)
        )
        
    def pet_name_exists(self, couple_id: UUID, pet_name: str):
        return self.db.scalar(
            select(
                select(Pet)
                .where(
                    Pet.couple_id == couple_id,
                    Pet.name == pet_name
                )
                .exists()
            )
        )

    def create(self, *, name, pet_type, couple_id):
        pet = Pet(
            name=name,
            pet_type=pet_type,
            couple_id=couple_id,
        )
        self.db.add(pet)
        self.db.flush()
        return pet