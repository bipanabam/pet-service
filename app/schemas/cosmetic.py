from pydantic import BaseModel, ConfigDict
from app.models.pet_state import PetStageEnum
from app.models.pet_cosmetic import CosmeticTypeEnum, CosmeticRarityEnum
from uuid import UUID
from datetime import datetime

class PetCosmeticBase(BaseModel):
    id: UUID
    name: str
    type: CosmeticTypeEnum
    required_stage: PetStageEnum
    asset_key: str
    rarity: CosmeticRarityEnum
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True
    }
    
class PetCosmeticCatalog(BaseModel):
    results: list[PetCosmeticBase]
    count: int
    
    model_config = ConfigDict(from_attributes=True)