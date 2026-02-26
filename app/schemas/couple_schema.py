from pydantic import BaseModel, Field
import uuid

class CoupleBase(BaseModel):
    id: uuid.UUID = Field(..., description="ID of the couple")
    pair_id: str = Field(..., description="ID of the couple from Appwrite")
    partnerOne_id: str = Field(..., description="ID of the first partner")
    partnerTwo_id: str = Field(..., description="ID of the second partner")
    
class CoupleSync(BaseModel):
    pair_id: str
    # partnerOne_id: str
    # partnerTwo_id: str