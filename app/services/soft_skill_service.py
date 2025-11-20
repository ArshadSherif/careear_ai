from sqlalchemy.orm import Session
from datetime import datetime

from app.db.models import (
    SoftSkillQuestion,
    SoftSkillAnswer,
    SoftSkillResult,
)

from app.db.schemas import SoftSkillAnswerBatchIn

# -----------------------------------------------------
# FETCH PAGINATED QUESTIONS
# -----------------------------------------------------
def get_questions_paginated(db: Session, limit: int, offset: int):
    q = (
        db.query(SoftSkillQuestion)
        .filter(SoftSkillQuestion.is_active.is_(True))
    )

    total = q.count()

    items = (
        q.order_by(SoftSkillQuestion.sort_order)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


# -----------------------------------------------------
# SAVE BATCH ANSWERS
# -----------------------------------------------------
def save_answers_batch(db: Session, payload: SoftSkillAnswerBatchIn):
    for ans in payload.answers:
        existing = (
            db.query(SoftSkillAnswer)
            .filter_by(
                session_id=payload.session_id,
                question_id=ans.question_id
            )
            .first()
        )

        if existing:
            existing.answer = ans.answer
        else:
            db.add(
                SoftSkillAnswer(
                    session_id=payload.session_id,
                    question_id=ans.question_id,
                    answer=ans.answer,
                )
            )

    db.commit()



# -----------------------------------------------------
# GENERATE FINAL RESULT
# -----------------------------------------------------
def finalize_result(db: Session, session_id: str):
    rows = (
        db.query(SoftSkillAnswer, SoftSkillQuestion)
        .join(
            SoftSkillQuestion,
            SoftSkillQuestion.id == SoftSkillAnswer.question_id
        )
        .filter(SoftSkillAnswer.session_id == session_id)
        .all()
    )

    scores = {}

    for ans, q in rows:
        if ans.answer not in q.weights:
            continue

        for domain, weight in q.weights[ans.answer].items():
            scores[domain] = scores.get(domain, 0) + weight

    existing = (
        db.query(SoftSkillResult)
        .filter_by(session_id=session_id)
        .first()
    )

    if existing:
        existing.result = scores
        existing.completed_at = datetime.utcnow()
    else:
        db.add(
            SoftSkillResult(
                session_id=session_id,
                result=scores,
            )
        )

    db.commit()

    return {
        "session_id": session_id,
        "result": scores,
        "completed_at": datetime.utcnow(),
    }
