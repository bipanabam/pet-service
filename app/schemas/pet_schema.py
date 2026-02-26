from pydantic import BaseModel, ConfigDict
from app.models.pet import PetTypeEnum
from uuid import UUID

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
