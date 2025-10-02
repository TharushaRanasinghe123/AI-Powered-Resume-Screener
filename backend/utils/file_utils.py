import os
import aiofiles
from fastapi import UploadFile,HTTPException
import magic

ALLOWED_FILE_TYPES = {
    'application/pdf': '.pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
    'text/plain': '.txt'
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def validate_file(file: UploadFile):
    """Validate the uploaded file for type and size."""
    content = await file.read()
    if(len(content) > MAX_FILE_SIZE):
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 10 MB.")
    
    file_type = magic.from_buffer(content, mime=True)
    if file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    await file.seek(0)  # Reset file pointer after reading
    return file_type

async def save_uploaded_file(file: UploadFile, upload_dir: str, filename: str):
    """Save the uploaded file to the specified directory."""
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, filename)

    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    return file_path

def get_file_extension(file_type: str):
    """Get the file extension based on the MIME type."""
    return ALLOWED_FILE_TYPES.get(file_type, 'bin')

