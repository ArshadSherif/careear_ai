from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, schemas
from app.db.database import get_db
from app.services.assessment_service import score_resume
router = APIRouter()
@router.post("/", response_model=schemas.AssessmentRead)
def create_assessment(assessment_in: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    resume = crud.get_resume(db, assessment_in.resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    score = score_resume(db, assessment_in, db)
    return crud.create_assessment(db, assessment_in, score)
