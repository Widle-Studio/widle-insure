# Database Schema Documentation

The AI-Automated Auto Insurance Claims Platform is designed to run efficiently on PostgreSQL, leveraging UUIDs as primary keys, indexing critical columns (like claim numbers, policies, etc.), and securely tracking changes via an audit log.

## Overview

The database has three primary components:
1. `claims`: The core table containing information about a claim and claimant.
2. `claim_photos`: A table for storing metadata and AI analysis of claimant photos.
3. `claim_audit_log`: A table designed to keep a secure, non-repudiable history of claim lifecycle changes.

## Schema Details

```sql
-- Claims table
CREATE TABLE claims (
    id UUID PRIMARY KEY,
    policy_number VARCHAR(50) NOT NULL,
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    claimant_name VARCHAR(255),
    claimant_phone VARCHAR(20),
    claimant_email VARCHAR(255),
    incident_date TIMESTAMP,
    incident_location VARCHAR(500),
    incident_description TEXT,
    vehicle_vin VARCHAR(17),
    vehicle_make VARCHAR(100),
    vehicle_model VARCHAR(100),
    vehicle_year INT,
    status VARCHAR(50), -- pending, processing, approved, rejected
    estimated_damage_cost DECIMAL(10,2),
    approved_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Claim photos
CREATE TABLE claim_photos (
    id UUID PRIMARY KEY,
    claim_id UUID REFERENCES claims(id),
    photo_url VARCHAR(500),
    photo_type VARCHAR(50), -- front, rear, side, interior, damage
    ai_analysis JSONB, -- Store AI vision results
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Audit log
CREATE TABLE claim_audit_log (
    id UUID PRIMARY KEY,
    claim_id UUID REFERENCES claims(id),
    action VARCHAR(100),
    performed_by VARCHAR(100),
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## ORM

The backend platform leverages **SQLAlchemy**, standardizing mapping to this schema using standard Alembic migrations.

## Future Plans

The backend may eventually support:
* Policy tables, to hold active coverages instead of simple mocking.
* Dedicated Admin tables for Role-Based Access Control (RBAC).
* Additional data structures to track external payouts via Stripe (e.g. `payout_id`, `payout_status`).