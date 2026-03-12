from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, UUID, func

import uuid
from datetime import datetime, timedelta

from app.models import Pet, PetState, PetEvent, PetActivity, PetActivityParticipant, PetStageEnum
from app.services.activity_engine import ActivityEngine
from app.repositories.pet_repository import PetRepository
from app.schemas.pet import PetCreate

HATCH_TIME = timedelta(hours=6)
class PetService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.pet_repo = PetRepository(db)
        
    # async def refresh_state(self, pet, state):
    #     await self.maybe_hatch(pet, state)
    #     self.apply_stat_decay(state)

    async def maybe_hatch(self, pet: Pet, state: PetState):
        if state.stage != PetStageEnum.EGG:
            return False

        if datetime.utcnow() - pet.created_at >= HATCH_TIME:
            state.stage = PetStageEnum.BABY
            state.growth_level = 1
            state.updated_at = datetime.utcnow()

            await self.db.flush()
            await self.db.refresh(state)

            return True

        return False
    
    async def get_pet_state(self, pet_id: uuid.UUID, couple_id: uuid.UUID):
        pet = await self.pet_repo.get_by_id_and_couple(pet_id, couple_id)
        if not pet:
            return None

        state = pet.state
        # Handle egg hatch automatically
        await self.maybe_hatch(pet, state)
        
        return state

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
            stage=PetStageEnum.EGG,
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
        partner_id: str,
        idempotency_key: uuid.UUID,
    ):        
        # Idempotency guard
        event = PetEvent(
            id=idempotency_key,
            pet_id=pet_id,
            activity_id=activity_id,
        )
        try:
            self.db.add(event)
            await self.db.flush()
        except IntegrityError:
            # Request already processed
            return {"status": "Duplicate"}

        # Lock Activity
        result = await self.db.execute(
            select(PetActivity)
            .where(
                PetActivity.pet_id == pet_id,
                PetActivity.activity_id == activity_id,
            )
            .with_for_update()
        )

        activity = result.scalar_one_or_none()
        
        if not activity:
            activity = PetActivity(
                pet_id=pet_id,
                activity_type=activity_type,
                activity_id=activity_id,
            )
            self.db.add(activity)
            await self.db.flush()

        now = datetime.utcnow()
        
        # Insert participant completion
        completion = PetActivityParticipant(
            activity_id=activity.id,
            partner_id=partner_id,
        )

        try:
            self.db.add(completion)
            await self.db.flush()
        except IntegrityError:
            return {"status": "Already Completed"}
        
        # Count participants: Reward only when both complete
        result = await self.db.execute(
            select(func.count())
            .select_from(PetActivityParticipant)
            .where(PetActivityParticipant.activity_id == activity.id)
        )

        completion_count = result.scalar_one()
        if completion_count >= 2 and activity.xp_awarded == 0:
            state_result = await self.db.execute(
                select(PetState)
                .where(PetState.pet_id == pet_id)
                .with_for_update()
            )

            state = state_result.scalar_one()

            engine = ActivityEngine(state)
            result_data = engine.apply(activity_type)

            activity.xp_awarded = result_data["xp_gained"]
            
            return {
                "status": "completed_together",
                "result" : result_data
            }

        return {"status": "partner_completed"}