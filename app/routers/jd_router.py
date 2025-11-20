from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import jd_service

router = APIRouter()

@router.post("/", response_model=schemas.JobDescriptionRead)
def create_jd(
    jd_in: schemas.JobDescriptionCreate,
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    return jd_service.create_jd(db, jd_in, session_id)


@router.get("/{jd_id}", response_model=schemas.JobDescriptionRead)
def read_jd(jd_id: int, db: Session = Depends(get_db)):
    jd = jd_service.get_jd(db, jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="JD not found")
    return jd
