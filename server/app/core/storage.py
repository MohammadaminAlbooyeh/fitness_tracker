import os
from fastapi import UploadFile
import uuid
from typing import Optional

# Configuration for file uploads
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def upload_file(file: UploadFile, subdirectory: Optional[str] = None) -> str:
    """
    Upload a file to the server storage.
    
    Args:
        file: The file to upload
        subdirectory: Optional subdirectory to organize files (e.g., 'exercises', 'progress_photos')
    
    Returns:
        The file path where the file was saved
    """
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(UPLOAD_DIR, subdirectory) if subdirectory else UPLOAD_DIR
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_path, unique_filename)
    
    # Save the file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return file_path
