from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import (
    SoftSkillQuestionPage,
    SoftSkillAnswerBatchIn,
    SoftSkillResultRead,
)
from app.services.soft_skill_service import (
    get_questions_paginated,
    save_answers_batch,
    finalize_result,
)
router = APIRouter(prefix="/soft-skills")


# -----------------------------------------------------
# GET PAGINATED QUESTIONS
# -----------------------------------------------------
@router.get("/questions", response_model=SoftSkillQuestionPage)
def list_questions(
    limit: int = 5,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return get_questions_paginated(db, limit, offset)


# -----------------------------------------------------
# SAVE BATCH ANSWERS
# -----------------------------------------------------
@router.post("/answers/batch")
def batch_answers(
    payload: SoftSkillAnswerBatchIn,
    db: Session = Depends(get_db)
):
    save_answers_batch(db, payload)
    return {"status": "ok"}


# -----------------------------------------------------
# GET FINAL RESULT
# -----------------------------------------------------
@router.get("/results", response_model=SoftSkillResultRead)
def get_result(
    session_id: str = Query(...),
    db: Session = Depends(get_db)
):
    return finalize_result(db, session_id)
