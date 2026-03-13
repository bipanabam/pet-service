from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pet_state import PetStageEnum
from app.services.cosmetic_service import CosmeticService

class ActivityEngine:

    ACTIVITY_MATRIX = {
        "feed_pet": {"xp": 10, "health": 5, "happiness": 3, "energy": 5},
        "go_on_walk": {"xp": 20, "health": 10, "happiness": 10, "energy": -5},
        "bathe_pet": {"xp": 15, "health": 8, "happiness": 5, "energy": -2},
        "cuddle_time": {"xp": 10, "health": 0, "happiness": 12, "energy": -3},
        # "daily_prayer": {"xp": 50, "health": 3, "happines": 5, "energy":0},
        # "cuddle_time":  {"xp": 10, "health": 0, "happines": 12, "energy":-3},
    }
    
    EVOLUTION_XP = {
        PetStageEnum.EGG: 50,
        PetStageEnum.BABY: 300,
        PetStageEnum.TEEN: 1000,
    }

    NEXT_STAGE = {
        PetStageEnum.EGG: PetStageEnum.BABY,
        PetStageEnum.BABY: PetStageEnum.TEEN,
        PetStageEnum.TEEN: PetStageEnum.ADULT,
    }


    def __init__(self, state, db: AsyncSession):
        self.state = state
        self.db = db
        self.cosmetic_service = CosmeticService(db)
        
    def _handle_evolution(self):
        current_stage = self.state.stage
        threshold = self.EVOLUTION_XP.get(current_stage)

        if threshold and self.state.xp >= threshold:
            self.state.stage = self.NEXT_STAGE[current_stage]
            self.state.growth_level += 1
            return True
        return False
            
    def _handle_growth(self):
        if self.state.xp > self.state.growth_level * 200:
            self.state.growth_level += 1
            
    async def apply(self, activity_type: str):
        config = self.ACTIVITY_MATRIX.get(activity_type)
        if not config:
            raise ValueError("Invalid activity")

        self.state.xp += config["xp"]
        self.state.health = min(100, self.state.health + config["health"])
        self.state.happiness = min(100, self.state.happiness + config["happiness"])
        self.state.energy = max(0, self.state.energy + config["energy"])

        evolved = self._handle_evolution()
        self._handle_growth()
        
        # unlock cosmetics automatically after evolution
        if evolved:
            await self.cosmetic_service.unlock_stage_rewards(self.state.pet)

        return {
            "xp_gained": config["xp"],
            "new_growth_level": self.state.growth_level,
            "stage": self.state.stage,
            "new_health": self.state.health,
            "mood": self.state.mood,
        }