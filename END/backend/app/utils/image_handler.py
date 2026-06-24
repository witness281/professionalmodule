import os
import shutil
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.core.config import settings
import uuid

UPLOAD_DIR = "frontend/assets/images"

def validate_image(file: UploadFile):
    if file.size > settings.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image too large (max 2MB)")
    
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type")

def save_book_image(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # Сохраняем и сжимаем изображение
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Изменяем размер
    img = Image.open(filepath)
    img.thumbnail((settings.IMAGE_MAX_WIDTH, settings.IMAGE_MAX_HEIGHT))
    img.save(filepath, optimize=True, quality=85)
    
    return f"/assets/images/{filename}"