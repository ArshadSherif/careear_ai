from sqlalchemy.orm import Session
from app.db import crud, schemas
def score_resume(db: Session, payload: schemas.AssessmentCreate, session: Session = None) -> int:
    resume = crud.get_resume(db, payload.resume_id)
    if not resume:
        return 0
    text = (resume.text or "").lower()
    keywords = ["python", "sql", "fastapi", "docker", "aws", "tensorflow", "pytorch"]
    raw_score = sum(text.count(k) for k in keywords)
    score = min(100, raw_score * 10)
    return score
