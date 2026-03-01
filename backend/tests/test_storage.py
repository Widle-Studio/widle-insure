import os
import shutil
from unittest.mock import patch, MagicMock, mock_open
from io import BytesIO
from fastapi import UploadFile
import pytest

from app.services.storage import StorageService, UPLOAD_DIR

@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.os.path.exists")
def test_storage_service_init_creates_dir(mock_exists, mock_makedirs):
    # Setup
    mock_exists.return_value = False

    # Execute
    StorageService()

    # Assert
    mock_exists.assert_called_once_with(UPLOAD_DIR)
    mock_makedirs.assert_called_once_with(UPLOAD_DIR)

@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.os.path.exists")
def test_storage_service_init_does_not_create_dir(mock_exists, mock_makedirs):
    # Setup
    mock_exists.return_value = True

    # Execute
    StorageService()

    # Assert
    mock_exists.assert_called_once_with(UPLOAD_DIR)
    mock_makedirs.assert_not_called()

@pytest.mark.asyncio
@patch("app.services.storage.shutil.copyfileobj")
@patch("builtins.open", new_callable=mock_open)
@patch("app.services.storage.uuid4")
@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.os.path.exists")
async def test_upload_file(mock_exists, mock_makedirs, mock_uuid4, m_open, mock_copyfileobj):
    # Setup
    mock_exists.return_value = True
    mock_uuid4.return_value = "1234-5678"

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.jpg"
    mock_file.file = MagicMock()

    # Execute
    service = StorageService()
    file_path = await service.upload_file(mock_file)

    # Assert
    expected_file_path = os.path.join(UPLOAD_DIR, "1234-5678.jpg")
    assert file_path == expected_file_path

    m_open.assert_called_once_with(expected_file_path, "wb")

    # Verify copyfileobj uses the file object created by open
    mock_copyfileobj.assert_called_once_with(mock_file.file, m_open())
