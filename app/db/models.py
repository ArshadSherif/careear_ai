from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON , Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from sqlalchemy.sql import func

# -----------------------------------------------------
# RESUME  MODELS
# -----------------------------------------------------

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, default="default")
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=True)

    skills = Column(JSON, nullable=True)
    traits = Column(JSON, nullable=True)
    domains = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)


# -----------------------------------------------------
# JOB DESCRIPTION MODELS
# -----------------------------------------------------

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, default="default")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    required_skills = Column(JSON, nullable=True)
    jd_traits = Column(JSON, nullable=True)
    jd_domains = Column(JSON, nullable=True)
    jd_seniority = Column(Integer, nullable=True)


# -----------------------------------------------------
# ASSESSMENT MODELS
# -----------------------------------------------------

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"))
    score = Column(Integer, default=0)
    details = Column(Text, nullable=True)


# -----------------------------------------------------
# SOFT SKILL MODELS
# -----------------------------------------------------
class SoftSkillQuestion(Base):
    __tablename__ = "soft_skill_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    options = Column(JSON, nullable=False)    # ["Agree","Neutral","Disagree"]
    weights = Column(JSON, nullable=False)    # { "Agree": {...}, "Neutral": {...} }
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class SoftSkillAnswer(Base):
    __tablename__ = "soft_skill_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(128), index=True, nullable=False)
    question_id = Column(Integer, nullable=False)
    answer = Column(String(32), nullable=False)   # "Agree" / "Neutral" / "Disagree"


class SoftSkillResult(Base):
    __tablename__ = "soft_skill_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(128), unique=True, nullable=False)
    result = Column(JSON, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    completed_at = Column(DateTime(timezone=True), default=datetime.utcnow)


# -----------------------------------------------------
# TECHNICAL SKILL QUESTIONS MODELS
# -----------------------------------------------------

class TechnicalDomainQuestions(Base):
    __tablename__ = "technical_domains"

    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(200), unique=True, nullable=False)
    tree = Column(JSON, nullable=False)   # full decision tree in JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())