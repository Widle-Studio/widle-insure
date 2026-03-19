from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class AdminUserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUserUpdate(AdminUserBase):
    password: Optional[str] = None

class AdminUserResponse(AdminUserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
