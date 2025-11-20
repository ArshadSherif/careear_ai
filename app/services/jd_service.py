from sqlalchemy.orm import Session
from app.db import models, schemas
from app.services.ai_services.jd_parsing_service import parse_jd_vectors


def create_jd(db: Session, jd_in: schemas.JobDescriptionCreate, session_id: str):
    vectors = parse_jd_vectors(jd_in.description)

    db_jd = models.JobDescription(
        title=jd_in.title,
        description=jd_in.description,
        required_skills=vectors["required_skills"],
        jd_traits=vectors["jd_traits"],
        jd_domains=vectors["jd_domains"],
        jd_seniority=vectors["jd_seniority"],
        session_id=session_id
    )

    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)
    return db_jd


def get_jd(db: Session, jd_id: int):
    return db.query(models.JobDescription).filter(models.JobDescription.id == jd_id).first()
