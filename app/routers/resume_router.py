from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import resume_service

router = APIRouter()

@router.post("/upload", response_model=schemas.ResumeRead)
async def upload_resume(
    file: UploadFile = File(...),
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    return await resume_service.handle_upload(db, file, session_id)


@router.get("/", response_model=list[schemas.ResumeRead])
def list_resumes(
    session_id: str = "default",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return resume_service.list_resumes(db, session_id, skip, limit)


@router.get("/{resume_id}", response_model=schemas.ResumeRead)
def get_resume(
    resume_id: int,
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    resume = resume_service.get_resume(db, resume_id, session_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
