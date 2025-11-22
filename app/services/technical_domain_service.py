# app/services/technical_domain_service.py

from sqlalchemy.orm import Session
from app.db import models
from app.services.ai_services.domain_classifer import classify_domain_ai


def load_all_domain_names(db: Session) -> list[str]:
    rows = db.query(models.TechnicalDomainQuestions.domain_name).all()
    return [r[0] for r in rows]


def load_resume_domains(db: Session, session_id: str) -> dict:
    resume = (
        db.query(models.Resume)
        .filter(models.Resume.session_id == session_id)
        .first()
    )
    return resume.domains if resume and resume.domains else {}


def load_jd_domains(db: Session, session_id: str) -> dict:
    jd = (
        db.query(models.JobDescription)
        .filter(models.JobDescription.session_id == session_id)
        .first()
    )
    return jd.jd_domains if jd and jd.jd_domains else {}


def load_soft_domains(db: Session, session_id: str) -> dict:
    row = (
        db.query(models.SoftSkillResult)
        .filter(models.SoftSkillResult.session_id == session_id)
        .first()
    )
    return row.result if row else {}


def derive_technical_domain(db: Session, session_id: str):
    resume_domains = load_resume_domains(db, session_id)
    jd_domains = load_jd_domains(db, session_id)
    soft_domains = load_soft_domains(db, session_id)
    allowed_domains = load_all_domain_names(db)

    # AI now returns scores for all domains
    scores = classify_domain_ai(
        resume_domains,
        jd_domains,
        soft_domains,
        allowed_domains
    )
    # scores format: {"Computer & Data Science": 0.92, "Engineering": 0.87, ...}

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top3 = ranked[:3]

    # Validate each domain exists in allowed list
    for d, _ in top3:
        if d not in allowed_domains:
            raise ValueError(f"AI returned invalid domain: {d}")

    return {
        "session_id": session_id,
        "top_domains": [
            {"domain": d, "score": s}
            for d, s in top3
        ]
    }


def get_domain_tree_service(db: Session, domain_name: str):
    row = (
        db.query(models.TechnicalDomainQuestions)
        .filter(models.TechnicalDomainQuestions.domain_name == domain_name)
        .first()
    )

    if not row:
        return {
            "domain_name": domain_name,
            "tree": None,
            "error": "Domain not found"
        }

    return {
        "domain_name": domain_name,
        "tree": row.tree
    }
