import pytest
from datetime import datetime, timezone

class SharedMockScalars:
    def __init__(self, result):
        self.result = result

    def first(self):
        if callable(self.result):
            return self.result()
        return self.result

class SharedMockResult:
    def __init__(self, result):
        self.result = result

    def scalars(self):
        return SharedMockScalars(self.result)

class SharedMockDbSession:
    def __init__(self, execute_result=None):
        self.added = []
        self.execute_result = execute_result

    def add(self, item):
        self.added.append(item)

    async def commit(self):
        pass

    async def refresh(self, item):
        item.id = "123e4567-e89b-12d3-a456-426614174000"
        item.created_at = datetime.now(timezone.utc)
        item.updated_at = datetime.now(timezone.utc)

    async def execute(self, stmt):
        if callable(self.execute_result):
            return SharedMockResult(self.execute_result(self, stmt))
        if self.execute_result is not None:
            return SharedMockResult(self.execute_result)

        # Default behavior: return the last added item with photos=[] initialized if missing
        def get_last_added():
            item = self.added[-1] if self.added else None
            if item:
                if not hasattr(item, "photos"):
                    item.photos = []
            return item
        return SharedMockResult(get_last_added)

@pytest.fixture
def mock_db_session():
    return SharedMockDbSession

@pytest.fixture
def mock_claim_class():
    class SharedMockClaim:
        def __init__(self, claim_id, payload):
            self.id = claim_id
            self.policy_number = payload.get("policy_number", "POL-123456789")
            incident_date = payload.get("incident_date", "2024-01-01T12:00:00")
            self.incident_date = datetime.fromisoformat(incident_date).replace(tzinfo=timezone.utc)
            self.incident_location = payload.get("incident_location", "New York, NY")
            self.incident_description = payload.get("incident_description", "Fender bender at intersection")
            self.vehicle_vin = payload.get("vehicle_vin", "1HGCM82633A004123")
            self.vehicle_make = payload.get("vehicle_make", "Honda")
            self.vehicle_model = payload.get("vehicle_model", "Accord")
            self.vehicle_year = payload.get("vehicle_year", 2022)
            self.claimant_name = payload.get("claimant_name", "John Doe")
            self.claimant_email = payload.get("claimant_email", "john.doe@example.com")
            self.claimant_phone = payload.get("claimant_phone", "555-0123")
            self.status = "New"
            self.claim_number = "CLM-2024-001234"
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)
            self.photos = []
    return SharedMockClaim
