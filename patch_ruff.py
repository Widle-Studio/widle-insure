import re

with open("backend/alembic/env.py", "r") as f:
    content = f.read()
if "import os\n\ndatabase_url" in content:
    content = "import os\n" + content.replace("import os\n\ndatabase_url", "\ndatabase_url")
    with open("backend/alembic/env.py", "w") as f:
        f.write(content)

with open("backend/app/api/v1/endpoints/claims.py", "r") as f:
    content = f.read()
if "photo_urls =" in content:
    content = re.sub(r'\s*# Get photo URLs\s*photo_urls = \[.*?\]', '', content)
    with open("backend/app/api/v1/endpoints/claims.py", "w") as f:
        f.write(content)

with open("backend/app/api/v1/endpoints/health.py", "r") as f:
    content = f.read()
if "except:" in content:
    content = content.replace("except:", "except Exception:")
    with open("backend/app/api/v1/endpoints/health.py", "w") as f:
        f.write(content)

with open("backend/app/api/v1/endpoints/payments.py", "r") as f:
    content = f.read()
content = content.replace("transfer_id = f\"tr_{secrets.token_hex(12)}\"", "_transfer_id = f\"tr_{secrets.token_hex(12)}\"")
content = content.replace("raise HTTPException(status_code=502, detail=f\"Payment gateway error: {e.user_message}\")", "raise HTTPException(status_code=502, detail=f\"Payment gateway error: {e.user_message}\") from e")
content = content.replace("raise HTTPException(status_code=500, detail=\"Internal server error during payout\")", "raise HTTPException(status_code=500, detail=\"Internal server error during payout\") from e")
with open("backend/app/api/v1/endpoints/payments.py", "w") as f:
    f.write(content)

with open("backend/app/main.py", "r") as f:
    content = f.read()
content = content.replace("import time\n\nfrom fastapi import Request", "")
content = "import time\nfrom fastapi import Request\n" + content
content = content.replace("from app.api.v1.endpoints import payments\nfrom app.api.v1.endpoints.admin import auth as admin_auth\nfrom app.api.v1.endpoints.admin import claims as admin_claims\nfrom app.api.v1.endpoints.health import router as health_router", "")
content = "from app.api.v1.endpoints import payments\nfrom app.api.v1.endpoints.admin import auth as admin_auth\nfrom app.api.v1.endpoints.admin import claims as admin_claims\nfrom app.api.v1.endpoints.health import router as health_router\n" + content
with open("backend/app/main.py", "w") as f:
    f.write(content)

with open("backend/tests/test_cors.py", "r") as f:
    content = f.read()
content = content.replace("from fastapi.testclient import TestClient", "")
content = "from fastapi.testclient import TestClient\n" + content
with open("backend/tests/test_cors.py", "w") as f:
    f.write(content)

with open("backend/tests/test_email.py", "r") as f:
    content = f.read()
content = content.replace("if attr == \"RESEND_API_KEY\": return \"test_key\"", "if attr == \"RESEND_API_KEY\":\n                return \"test_key\"")
content = content.replace("if attr == \"EMAIL_FROM\": return \"test@example.com\"", "if attr == \"EMAIL_FROM\":\n                return \"test@example.com\"")
with open("backend/tests/test_email.py", "w") as f:
    f.write(content)

with open("backend/tests/test_logging.py", "r") as f:
    content = f.read()
content = content.replace("patch(\"app.core.log_config.logging.getLogger\") as mock_get_logger:", "patch(\"app.core.log_config.logging.getLogger\"):")
with open("backend/tests/test_logging.py", "w") as f:
    f.write(content)
