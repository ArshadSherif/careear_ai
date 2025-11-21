from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.db.database import engine, init_db
import os
from app.routers import (
    assessment_router,
    jd_router,
    resume_router,
    soft_skills_questions_router,
    technical_domain_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connected")
    except Exception as e:
        print("Database connection failed:", e)
        raise e
    init_db()
    yield  

    # Shutdown
    print("Shutting down...")

app = FastAPI(title="SkillDesk", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessment_router.router, prefix="/assessment", tags=["Assessment"])
app.include_router(jd_router.router, prefix="/jd", tags=["Job Description"])
app.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
app.include_router(soft_skills_questions_router.router, prefix="/questions", tags=["Questions"])
app.include_router(technical_domain_router.router, prefix="/technical", tags=["Technical Domain"])

@app.get("/")
def healthcheck():
    return {"status": "ok", "service": "SkillDesk"}
