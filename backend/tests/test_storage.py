import os
import pytest
from unittest.mock import patch, MagicMock, mock_open
from fastapi import UploadFile

from app.services.storage import StorageService

@patch("app.services.storage.os.path.exists")
@patch("app.services.storage.os.makedirs")
def test_storage_service_init_creates_dir(mock_makedirs, mock_exists):
    """Test that the upload directory is created if it does not exist."""
    mock_exists.return_value = False
    StorageService()
    mock_exists.assert_called_once_with("uploads")
    mock_makedirs.assert_called_once_with("uploads")

@patch("app.services.storage.os.path.exists")
@patch("app.services.storage.os.makedirs")
def test_storage_service_init_dir_exists(mock_makedirs, mock_exists):
    """Test that the upload directory is not created if it already exists."""
    mock_exists.return_value = True
    StorageService()
    mock_exists.assert_called_once_with("uploads")
    mock_makedirs.assert_not_called()

@pytest.mark.asyncio
@patch("app.services.storage.os.path.exists")
@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.uuid4")
@patch("app.services.storage.shutil.copyfileobj")
@patch("builtins.open", new_callable=mock_open)
async def test_upload_file(mock_file, mock_copy, mock_uuid, mock_makedirs, mock_exists):
    """Test that a file is uploaded and saved with a new UUID and correct extension."""
    mock_uuid.return_value = "12345678-1234-5678-1234-567812345678"

    # Mock FastAPI UploadFile
    mock_upload_file = MagicMock(spec=UploadFile)
    mock_upload_file.filename = "test_image.jpg"
    mock_upload_file.file = MagicMock()

    service = StorageService()

    file_path = await service.upload_file(mock_upload_file)

    # Check that the file was opened for writing in binary mode
    expected_path = os.path.join("uploads", "12345678-1234-5678-1234-567812345678.jpg")
    mock_file.assert_called_once_with(expected_path, "wb")

    # Check that shutil.copyfileobj was called with the file stream and the opened file
    mock_copy.assert_called_once_with(mock_upload_file.file, mock_file.return_value)

    # Check that the returned path is correct
    assert file_path == expected_path

@pytest.mark.asyncio
@patch("app.services.storage.os.path.exists")
@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.uuid4")
@patch("app.services.storage.shutil.copyfileobj")
@patch("builtins.open", new_callable=mock_open)
async def test_upload_file_no_extension(mock_file, mock_copy, mock_uuid, mock_makedirs, mock_exists):
    """Test uploading a file that has no extension."""
    mock_uuid.return_value = "87654321-4321-8765-4321-876543210987"

    mock_upload_file = MagicMock(spec=UploadFile)
    mock_upload_file.filename = "test_file_without_extension"
    mock_upload_file.file = MagicMock()

    service = StorageService()

    file_path = await service.upload_file(mock_upload_file)

    expected_path = os.path.join("uploads", "87654321-4321-8765-4321-876543210987")
    mock_file.assert_called_once_with(expected_path, "wb")

    assert file_path == expected_path
