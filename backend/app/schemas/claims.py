from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


from pydantic import Field, validator
import re

class ClaimBase(BaseModel):
    policy_number: str = Field(..., min_length=1, max_length=50)
    incident_date: datetime
    incident_location: str = Field(..., min_length=1, max_length=500)
    incident_description: str = Field(..., min_length=1)
    vehicle_vin: Optional[str] = Field(None, min_length=17, max_length=17)
    vehicle_make: str = Field(..., min_length=1, max_length=100)
    vehicle_model: str = Field(..., min_length=1, max_length=100)
    vehicle_year: int = Field(..., ge=1900, le=datetime.now().year + 1)
    claimant_name: str = Field(..., min_length=1, max_length=255)
    claimant_email: str = Field(..., pattern=r"^\S+@\S+\.\S+$")
    claimant_phone: str = Field(..., min_length=1, max_length=20)

    @validator("vehicle_vin")
    def validate_vin(cls, v):  # pylint: disable=no-self-argument
        if v is not None:
            # Basic VIN validation: alphanumeric, 17 chars, no I, O, Q
            if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", v.upper()):
                raise ValueError("Invalid VIN format")
            return v.upper()
        return v

    @validator("incident_date")
    def validate_incident_date(cls, v):  # pylint: disable=no-self-argument
        now = datetime.now(v.tzinfo)
        if v > now:
            raise ValueError("Incident date cannot be in the future")
        return v

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
