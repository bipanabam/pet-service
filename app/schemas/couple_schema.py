from pydantic import BaseModel, Field

class CoupleBase(BaseModel):
    id: str = Field(..., description="ID of the couple")
    partnerOne_id: str = Field(..., description="ID of the first partner")
    partnerTwo_id: str = Field(..., description="ID of the second partner")
    
class CoupleSync(BaseModel):
    pair_id: str
    # partnerOne_id: str
    # partnerTwo_id: str