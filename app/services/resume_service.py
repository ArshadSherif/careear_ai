import os, uuid, io
import pdfplumber, docx
from sqlalchemy.orm import Session

from app.db import models
from app.services.ai_services.resume_parsing_service import parse_resume_vectors

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "app/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _extract_text(filename: str, content: bytes) -> str:
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except:
            return ""

    if ext == "docx":
        try:
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except:
            return ""

    try:
        return content.decode("utf8", errors="ignore")
    except:
        return ""


def _save_file(file) -> tuple[str, bytes]:
    ext = os.path.splitext(file.filename)[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)
    content = file.file.read()

    with open(save_path, "wb") as f:
        f.write(content)

    return safe_name, content


async def handle_upload(db: Session, file, session_id: str) -> models.Resume:
    safe_filename, content = _save_file(file)
    text = _extract_text(file.filename, content)

    vectors = parse_resume_vectors(text)

    db_resume = models.Resume(
        filename=safe_filename,
        text=None,
        skills=vectors["skills"],
        traits=vectors["traits"],
        domains=vectors["domains"],
        experience=vectors["experience"],
        session_id=session_id
    )

    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def list_resumes(db: Session, skip: int, limit: int):
    return db.query(models.Resume).offset(skip).limit(limit).all()


def get_resume(db: Session, resume_id: int):
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()
