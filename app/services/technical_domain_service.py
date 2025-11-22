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
    # Load signals
    resume_domains = load_resume_domains(db, session_id)
    jd_domains = load_jd_domains(db, session_id)
    soft_domains = load_soft_domains(db, session_id)

    # Load allowed domain list (27)
    allowed_domains = load_all_domain_names(db)

    # AI picks the best domain
    selected_domain = classify_domain_ai(
        resume_domains,
        jd_domains,
        soft_domains,
        allowed_domains
    )

    # Safety validation
    if selected_domain not in allowed_domains:
        raise ValueError(f"AI returned invalid domain: {selected_domain}")


    return {
        "session_id": session_id,
        "selected_domain": selected_domain,
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
