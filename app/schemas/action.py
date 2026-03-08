from pydantic import BaseModel
from uuid import UUID
from app.models.pet_activity_log import ActivityTypeEnum

class PetActionRequest(BaseModel):
    activity_type: ActivityTypeEnum
    activity_id: UUID
    event_id: UUID