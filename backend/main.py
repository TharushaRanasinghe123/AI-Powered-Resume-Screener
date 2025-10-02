import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from utils.file_utils import validate_file, save_uploaded_file, get_file_extension  


app = FastAPI(
    title="Resume Scanner API", 
    description="AI-powered Resume Scanning and matching System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "backend/uploads"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume Scanner API","version":"1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Resume Scanner","timestamp": datetime.datetime.now().isoformat()}

# File upload endpoint for resumes
@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a resume file(PDF, DOCX, TXT)."""

    try:
        #validate file 
        file_type = await validate_file(file)

        #generate unique filename
        file_extension = get_file_extension(file_type)
        unique_filename = f"resume_{uuid.uuid4().hex}.{file_extension}"

        #save file
        upload_dir = os.path.join(UPLOAD_DIR, "resumes")
        file_path = await save_uploaded_file(file, upload_dir, unique_filename)  

        return JSONResponse({
            "message": "Resume uploaded successfully",
            "filename": unique_filename,
            "original_name": file.filename,
            "file_type": file_type,
            "file_size": os.path.getsize(file_path),
            "uploaded_at": datetime.datetime.now().isoformat()
        })  

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")  

    # File upload endpont for job description

@app.post("/upload/job_description")
async def upload_job_description(file: UploadFile = File(...)):

    """ Upload a job description file"""

    try:
        #validate file
        file_type = await validate_file(file)

        #generate unique filename
        file_extension = get_file_extension(file_type)
        unique_filename = f"jd_{uuid.uuid4().hex}.{file_extension}"   

        #save file
        upload_dir = os.path.join(UPLOAD_DIR, "job_descriptions")
        file_path = await save_uploaded_file(file, upload_dir, unique_filename)

        return JSONResponse({
            "message": "Job description uploaded successfully",
            "filename": unique_filename,
            "original_name": file.filename,
            "file_type": file_type,
            "file_size": os.path.getsize(file_path),
            "uploaded_at": datetime.datetime.now().isoformat()
        })

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    

@app.get("/files/resumes")
def list_resumes():
    """List all uploaded resumes."""
    
    upload_dir = os.path.join(UPLOAD_DIR, "resumes")
    if not os.path.exists(upload_dir):
        return {"resumes": []}
    
    files = []
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            files.append({
                "filename": filename,
                "size": os.path.getsize(file_path),
                "uploaded_time": datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
            })
        
    return {"resumes": files}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
