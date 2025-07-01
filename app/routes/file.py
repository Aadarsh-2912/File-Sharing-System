from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.utils.deps import require_ops_user, get_db, require_client_user
from sqlalchemy.orm import Session
from app.models.file import File as FileModel
import os
import shutil
from app.utils.s3 import upload_file_to_s3, generate_presigned_url

router = APIRouter(prefix="/files", tags=["files"])

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = File(...),
    current_user = Depends(require_ops_user),
    db: Session = Depends(get_db)
):
    filename = uploaded_file.filename
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed. Only pptx, docx, xlsx are permitted.")
    uploaded_file.file.seek(0)
    success = upload_file_to_s3(uploaded_file.file, filename, uploaded_file.content_type)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3.")
    file_record = FileModel(
        filename=filename,
        file_type=ext,
        user_id=current_user.id
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    return {"message": "File uploaded successfully", "file_id": file_record.id}

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    current_user = Depends(require_client_user),
    db: Session = Depends(get_db)
):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    download_url = generate_presigned_url(file_record.filename)
    return {"download-link": download_url, "message": "success"}

@router.get("/list")
def list_files(
    current_user = Depends(require_client_user),
    db: Session = Depends(get_db)
):
    files = db.query(FileModel).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "file_type": f.file_type,
            "uploaded_by": f.user_id,
            "upload_time": f.upload_time
        }
        for f in files
    ] 