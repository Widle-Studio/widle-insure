import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.services.storage import UPLOAD_DIR, StorageService


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
@patch("app.services.storage.aiofiles.open")
@patch("app.services.storage.uuid4")
@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.os.path.exists")
async def test_upload_file(mock_exists, mock_makedirs, mock_uuid4, mock_aiofiles_open):
    # Setup
    mock_exists.return_value = True
    mock_uuid4.return_value = "1234-5678"

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_image.jpg"

    # Mocking async read
    async def mock_read(size):
        if not hasattr(mock_read, 'called'):
            mock_read.called = True
            return b"dummy content"
        return b""
    mock_file.read = mock_read

    # Mocking aiofiles open
    mock_file_obj = AsyncMock()
    mock_aiofiles_open.return_value.__aenter__.return_value = mock_file_obj

    # Execute
    service = StorageService()
    file_path = await service.upload_file(mock_file)

    # Assert
    expected_file_path = os.path.join(UPLOAD_DIR, "1234-5678.jpg")
    assert file_path == expected_file_path

    mock_aiofiles_open.assert_called_once_with(expected_file_path, "wb")
    mock_file_obj.write.assert_called_once_with(b"dummy content")

@pytest.mark.asyncio
@patch("app.services.storage.aiofiles.open")
@patch("app.services.storage.uuid4")
@patch("app.services.storage.os.makedirs")
@patch("app.services.storage.os.path.exists")
@patch("app.services.storage.os.remove")
async def test_upload_file_exceeds_size_limit(mock_remove, mock_exists, mock_makedirs, mock_uuid4, mock_aiofiles_open):
    # Setup
    mock_exists.return_value = True
    mock_uuid4.return_value = "1234-5678"

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_large_image.jpg"

    # Mocking async read to return more than MAX_UPLOAD_SIZE
    async def mock_read(size):
        if not hasattr(mock_read, 'called'):
            mock_read.called = True
            return b"A" * (settings.MAX_UPLOAD_SIZE + 1)
        return b""
    mock_file.read = mock_read

    # Mocking aiofiles open
    mock_file_obj = AsyncMock()
    mock_aiofiles_open.return_value.__aenter__.return_value = mock_file_obj

    # Execute and Assert Exception
    service = StorageService()
    expected_file_path = os.path.join(UPLOAD_DIR, "1234-5678.jpg")

    with pytest.raises(HTTPException) as exc_info:
        await service.upload_file(mock_file)

    # Assert Status Code and Cleanup
    assert exc_info.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    # Assert os.remove was called to clean up the partial file
    # Ensure mock_exists returns True when checking for file cleanup
    mock_remove.assert_called_once_with(expected_file_path)
