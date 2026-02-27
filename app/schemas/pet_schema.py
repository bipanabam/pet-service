from pydantic import BaseModel, ConfigDict
from app.models.pet import PetTypeEnum
from app.models.pet_state import PetStageEnum
from uuid import UUID
from datetime import datetime

class PetBase(BaseModel):
    name: str
    pet_type: PetTypeEnum
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True
    }
    
class PetStateBase(BaseModel):
    stage: str
    xp: int
    health: int
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True
    }

class PetCreate(PetBase):
    pass
class PetCreateResponse(PetBase):
    id: UUID
    state: PetStateBase
    
    model_config = ConfigDict(from_attributes=True)
    
class PetList(BaseModel):
    results: list[PetCreateResponse]
    count: int
    
    model_config = ConfigDict(from_attributes=True)

class PetStateResponse(PetStateBase):
    pet_id: UUID
    name: str
    stage: PetStageEnum
    xp: int
    health: int
    growth_level: int
    happiness: int
    energy: int
    mood: str
    version: int
    last_interaction_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)