import shutil
import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

from fastapi import HTTPException
from PIL import Image
import io

class StorageService:
    def __init__(self):
        self.upload_dir = os.path.join(os.getcwd(), UPLOAD_DIR)
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    async def upload_file(self, file: UploadFile) -> str:
        """
        Validates an image and saves it to local disk. Returns the relative file path.
        """
        MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB
        ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

        if file.content_type not in ALLOWED_TYPES:
             raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}")

        # Read the file to check size and validate image format
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
             raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")

        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # Seek back to 0 so the file can be saved or used again
        await file.seek(0)

        file_extension = os.path.splitext(file.filename)[1]
        if not file_extension:
            file_extension = ".jpg" # Default if none provided

        file_name = f"{uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, file_name)

        # Write the file directly using aiofiles if available, else blockingly
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # Return relative URL pattern (e.g. /uploads/uuid.jpg)
        return f"/uploads/{file_name}"

storage_service = StorageService()
