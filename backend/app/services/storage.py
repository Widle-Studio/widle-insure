import asyncio
import os
import shutil
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
        # Early check for file size to prevent processing oversized files
        if file.size and file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds limit: {settings.MAX_UPLOAD_SIZE} bytes.",
            )

        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        try:
            if file.size:
                # Use efficient system-level copy when size is known and pre-validated
                await asyncio.to_thread(self._save_file_sync, file, file_path)
            else:
                # Fallback to chunked read if size is unknown
                await self._save_file_async_with_limit(file, file_path)
        except Exception:
            # Clean up partial file on failure
            if os.path.exists(file_path):
                os.remove(file_path)
            raise

        return file_path

    def _save_file_sync(self, file: UploadFile, dest_path: str) -> None:
        """Helper to perform synchronous file copy."""
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    async def _save_file_async_with_limit(
        self, file: UploadFile, dest_path: str
    ) -> None:
        """Fallback chunked upload with size validation when size is unknown."""
        accumulated_size = 0
        async with aiofiles.open(dest_path, "wb") as buffer:
            # Using smaller 64KB chunks for better memory efficiency
            while content := await file.read(64 * 1024):
                accumulated_size += len(content)
                if accumulated_size > settings.MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds limit: {settings.MAX_UPLOAD_SIZE} bytes.",
                    )
                await buffer.write(content)

    async def delete_file(self, file_path: str) -> None:
        """
        Deletes a file from local disk.
        """
        if os.path.exists(file_path):
            os.remove(file_path)


storage_service = StorageService()
