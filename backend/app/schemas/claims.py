import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


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

    @field_validator("vehicle_vin")
    @classmethod
    def validate_vin(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            # Basic VIN validation: alphanumeric, 17 chars, no I, O, Q
            if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", v.upper()):
                raise ValueError("Invalid VIN format")
            return v.upper()
        return v

    @field_validator("incident_date")
    @classmethod
    def validate_incident_date(cls, v: datetime) -> datetime:
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

    model_config = ConfigDict(from_attributes=True)

class ClaimResponse(ClaimBase):
    id: UUID
    claim_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    photos: List[ClaimPhotoResponse] = []

    model_config = ConfigDict(from_attributes=True)
