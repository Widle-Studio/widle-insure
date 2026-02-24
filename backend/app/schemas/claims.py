from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ClaimBase(BaseModel):
    policy_number: str
    incident_date: datetime
    incident_location: str
    incident_description: str
    vehicle_vin: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: int
    claimant_name: str
    claimant_email: str
    claimant_phone: str

class ClaimCreate(ClaimBase):
    pass

class ClaimPhotoResponse(BaseModel):
    id: UUID
    photo_url: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ClaimResponse(ClaimBase):
    id: UUID
    claim_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    photos: List[ClaimPhotoResponse] = []

    class Config:
        from_attributes = True
