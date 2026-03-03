from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, UUID
from sqlalchemy.orm import Session
from app.models import Pet, PetState, PetEvent
from app.services.activity_engine import ActivityEngine
from app.repositories.pet_repository import PetRepository
from app.schemas.pet import PetCreate
import uuid

class PetService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.pet_repo = PetRepository(db)

    async def create_pet(
        self, 
        couple_id: UUID, 
        payload: PetCreate
    ):

        if await self.pet_repo.count_by_couple(couple_id) >= 3:
            raise ValueError("Maximum pets reached")
            
        if await self.pet_repo.pet_name_exists(couple_id, payload.name):
            raise ValueError("Name already given to another pet.")

        pet = await self.pet_repo.create(
            name=payload.name,
            pet_type=payload.pet_type,
            couple_id=couple_id,
        )

        state = PetState(
            pet_id=pet.id,
            stage="egg",
            xp=0,
            health=100,
            growth_level=1,
            happiness=100,
            energy=100,
            version=1,
        )

        self.db.add(state)
        pet.state = state

        return pet
    
    async def process_action(
        self,
        *,
        pet_id: uuid.UUID,
        activity_type: str,
        activity_id: uuid.UUID,
        idempotency_key: uuid.UUID,
    ):
        # Idempotency guard
        event = PetEvent(
            id=idempotency_key,
            pet_id=pet_id,
            activity_id=activity_id,
        )
        self.db.add(event)

        # If duplicate → IntegrityError → rollback

        # Lock state row
        result = await self.db.execute(
            select(PetState)
            .where(PetState.pet_id == pet_id)
            .with_for_update()
        )
        state = result.scalar_one()

        # Apply engine (sync is fine)
        engine = ActivityEngine(state)
        result_data = engine.apply(activity_type)

        state.version += 1

        return result_data