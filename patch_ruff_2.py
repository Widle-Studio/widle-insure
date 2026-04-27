import re

with open("backend/app/api/v1/endpoints/payments.py", "r") as f:
    content = f.read()
content = content.replace("transfer_id = transfer.id", "_transfer_id = transfer.id")
with open("backend/app/api/v1/endpoints/payments.py", "w") as f:
    f.write(content)

with open("backend/tests/test_logging.py", "r") as f:
    content = f.read()
content = content.replace("patch(\"app.core.log_config.logging.getLogger\"):", "patch(\"app.core.log_config.logging.getLogger\") as mock_get_logger:")
content = content.replace("patch(\"app.core.log_config.logging.getLogger\") as mock_get_logger:", "patch(\"app.core.log_config.logging.getLogger\") as _mock_get_logger:", 1) # first one only
with open("backend/tests/test_logging.py", "w") as f:
    f.write(content)
