from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models, schemas

def list_resumes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Resume]:
    return db.query(models.Resume).offset(skip).limit(limit).all()
def create_assessment(db: Session, assessment_in: schemas.AssessmentCreate, score: int = 0):
    db_assessment = models.Assessment(resume_id=assessment_in.resume_id, details=assessment_in.details, score=score)
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment
def list_assessments(db: Session, resume_id: int = None):
    q = db.query(models.Assessment)
    if resume_id is not None:
        q = q.filter(models.Assessment.resume_id == resume_id)
    return q.all()
