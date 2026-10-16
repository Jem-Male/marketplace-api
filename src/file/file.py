from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import FileResponse

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
DIR = Path("./data/images")


class File:
    @staticmethod
    async def create_image(upload_file: UploadFile) -> str:
        file_extension = Path(upload_file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "File extension not allowed"
            )
        filename = f"{uuid4()}{file_extension}"
        file_path = DIR / filename
        content = await upload_file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
            
        return str(filename)
    
    
    @staticmethod
    async def get_image(image_uuid: str):
        if "/" in image_uuid or "\\":
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Invalid filename"
            )
        image_path = DIR / image_uuid
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(image_path)