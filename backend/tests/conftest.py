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
