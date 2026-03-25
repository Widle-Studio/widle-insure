import pytest
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError
from app.schemas.claims import ClaimCreate

def get_valid_claim_data():
    return {
        "policy_number": "POL-12345",
        "incident_date": datetime.now(timezone.utc) - timedelta(days=1),
        "incident_location": "123 Main St, Anytown, USA",
        "incident_description": "Car accident at intersection",
        "vehicle_vin": "1HGCM82633A004123",
        "vehicle_make": "Honda",
        "vehicle_model": "Accord",
        "vehicle_year": 2022,
        "claimant_name": "John Doe",
        "claimant_email": "john.doe@example.com",
        "claimant_phone": "555-0123",
    }

def test_valid_claim():
    data = get_valid_claim_data()
    # Test lowercase VIN conversion to uppercase
    data["vehicle_vin"] = "1hgcm82633a004123"
    claim = ClaimCreate(**data)
    assert claim.vehicle_vin == "1HGCM82633A004123"
    assert claim.policy_number == data["policy_number"]

def test_vin_validation():
    data = get_valid_claim_data()

    # Test invalid length (too short)
    data["vehicle_vin"] = "1234567890123456"
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "String should have at least 17 characters" in str(excinfo.value)

    # Test invalid length (too long)
    data["vehicle_vin"] = "123456789012345678"
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "String should have at most 17 characters" in str(excinfo.value)

    # Test invalid characters (I, O, Q)
    data["vehicle_vin"] = "1HGCM82633A004I23" # Contains I
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Invalid VIN format" in str(excinfo.value)

    data["vehicle_vin"] = "1HGCM82633A004O23" # Contains O
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Invalid VIN format" in str(excinfo.value)

    data["vehicle_vin"] = "1HGCM82633A004Q23" # Contains Q
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Invalid VIN format" in str(excinfo.value)

    # Test None value (Optional)
    data["vehicle_vin"] = None
    claim = ClaimCreate(**data)
    assert claim.vehicle_vin is None

def test_incident_date_validation():
    data = get_valid_claim_data()

    # Test past date (valid)
    data["incident_date"] = datetime.now(timezone.utc) - timedelta(days=1)
    claim = ClaimCreate(**data)
    assert claim.incident_date == data["incident_date"]

    # Test future date (invalid)
    data["incident_date"] = datetime.now(timezone.utc) + timedelta(days=1)
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Incident date cannot be in the future" in str(excinfo.value)

def test_vehicle_year_validation():
    data = get_valid_claim_data()

    # Test year before 1900
    data["vehicle_year"] = 1899
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Input should be greater than or equal to 1900" in str(excinfo.value)

    # Test year too far in the future
    data["vehicle_year"] = datetime.now().year + 2
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert f"Input should be less than or equal to {datetime.now().year + 1}" in str(excinfo.value)

def test_email_validation():
    data = get_valid_claim_data()

    # Test invalid email
    data["claimant_email"] = "invalid-email"
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    # Pydantic V2 error message might vary, but usually contains "valid email address"
    assert "value is not a valid email address" in str(excinfo.value).lower() or "An email address must have an @-sign." in str(excinfo.value)

def test_required_fields():
    data = get_valid_claim_data()

    # Test missing policy_number
    del data["policy_number"]
    with pytest.raises(ValidationError) as excinfo:
        ClaimCreate(**data)
    assert "Field required" in str(excinfo.value)
