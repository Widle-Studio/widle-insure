import shutil
import os
from uuid import uuid4
from fastapi import UploadFile

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

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

storage_service = StorageService()
