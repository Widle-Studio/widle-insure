from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ClaimStatusUpdate(BaseModel):
    status: str = Field(..., description="The new status for the claim (e.g. approved, rejected, processing, pending)")
    notes: Optional[str] = Field(None, description="Optional notes or reasons for the status update")

    model_config = ConfigDict(from_attributes=True)

class ClaimActionResponse(BaseModel):
    message: str
    claim_id: str
    status: str

    model_config = ConfigDict(from_attributes=True)
