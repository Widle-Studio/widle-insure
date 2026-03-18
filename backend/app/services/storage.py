import os
from uuid import uuid4

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

UPLOAD_DIR = "uploads"

class StorageService:
    def __init__(self):
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

    async def upload_file(self, file: UploadFile) -> str:
        """
        Saves a file to local disk and returns the file path.
        """
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        accumulated_size = 0

        try:
            async with aiofiles.open(file_path, "wb") as buffer:
                # Read in chunks to avoid memory issues with large files
                while content := await file.read(1024 * 1024):  # 1MB chunks
                    accumulated_size += len(content)
                    # Prevent DoS attacks by validating the accumulated chunk size limit
                    if accumulated_size > settings.MAX_UPLOAD_SIZE:
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"Upload rejected: File exceeds the maximum allowed size limit of {settings.MAX_UPLOAD_SIZE} bytes."
                        )
                    await buffer.write(content)
        except Exception:
            # Clean up partial file on failure
            if os.path.exists(file_path):
                os.remove(file_path)
            raise

        return file_path

    async def delete_file(self, file_path: str) -> None:
        """
        Deletes a file from local disk.
        """
        if os.path.exists(file_path):
            os.remove(file_path)

storage_service = StorageService()
