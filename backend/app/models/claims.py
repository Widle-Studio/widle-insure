import uuid

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_number = Column(String, nullable=False, index=True)
    claim_number = Column(String, unique=True, nullable=False, index=True)
    claimant_name = Column(String, nullable=True)
    claimant_phone = Column(String, nullable=True)
    claimant_email = Column(String, nullable=True)
    incident_date = Column(DateTime, nullable=True)
    incident_location = Column(String, nullable=True)
    incident_description = Column(Text, nullable=True)
    vehicle_vin = Column(String, nullable=True)
    vehicle_make = Column(String, nullable=True)
    vehicle_model = Column(String, nullable=True)
    vehicle_year = Column(Integer, nullable=True)
    status = Column(String, default="pending", index=True)
    estimated_damage_cost = Column(Numeric(10, 2), nullable=True)
    approved_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    photos = relationship(
        "ClaimPhoto", back_populates="claim", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "ClaimAuditLog", back_populates="claim", cascade="all, delete-orphan"
    )

class ClaimPhoto(Base):
    __tablename__ = "claim_photos"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(Uuid(as_uuid=True), ForeignKey("claims.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    photo_type = Column(String, nullable=True)
    ai_analysis = Column(JSON, nullable=True)
    uploaded_at = Column(DateTime, default=func.now())

    claim = relationship("Claim", back_populates="photos")

class ClaimAuditLog(Base):
    __tablename__ = "claim_audit_log"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = Column(Uuid(as_uuid=True), ForeignKey("claims.id"), nullable=False)
    action = Column(String, nullable=False)
    performed_by = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

    claim = relationship("Claim", back_populates="audit_logs")
