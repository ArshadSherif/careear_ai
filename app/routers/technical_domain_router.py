# app/routers/technical_domain_router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.technical_domain_service import derive_technical_domain, get_domain_tree_service

router = APIRouter()

@router.get("/select")
def select_domain(session_id: str = Query(...), db: Session = Depends(get_db)):
    return derive_technical_domain(db, session_id)

@router.get("/tree")
def get_domain_tree(
    domain_name: str = Query(...),
    db: Session = Depends(get_db)
):
    return get_domain_tree_service(db, domain_name)