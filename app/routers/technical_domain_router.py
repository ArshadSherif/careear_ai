# app/routers/technical_domain_router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.technical_domain_service import derive_technical_domain

router = APIRouter(prefix="/technical", tags=["Technical Domain"])


@router.get("/select")
def select_domain(
    session_id: str = Query(...),
    db: Session = Depends(get_db)
):
    return derive_technical_domain(db, session_id)
