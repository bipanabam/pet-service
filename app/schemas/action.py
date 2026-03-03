from pydantic import BaseModel
from uuid import UUID

class PetActionRequest(BaseModel):
    activity_type: str
    activity_id: UUID