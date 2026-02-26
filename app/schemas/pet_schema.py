from pydantic import BaseModel

class PetBase(BaseModel):
    id: str
    name: str
    pet_type: str
    is_active: bool = True
    
class PetList(BaseModel):
    results: list[PetBase]
    count: int

class PetCreate(PetBase):
    name: str
    pet_type: str
    
class PetCreateResponse(PetBase):
    id: str
    name: str
    pet_type: str
    initial_stage: str
    health: int
    xp: int