from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime 
from typing import List, Dict
# -----------------------------------------------------
# RESUME SCHEMAS
# -----------------------------------------------------

class ResumeCreate(BaseModel):
    filename: str
    text: str | None = None
    session_id: str = "default"


class ResumeRead(ResumeCreate):
    id: int
    uploaded_at: datetime | None = None
    skills: dict | None = None
    traits: dict | None = None
    domains: dict | None = None
    experience: dict | None = None

    model_config = {"from_attributes": True}

# -----------------------------------------------------
# JD SCHEMAS
# -----------------------------------------------------


class JobDescriptionCreate(BaseModel):
    title: str
    description: str
    session_id: str = "default"


class JobDescriptionRead(JobDescriptionCreate):
    id: int

    required_skills: dict | None = None
    jd_traits: dict | None = None
    jd_domains: dict | None = None
    jd_seniority: int | None = None

    model_config = {"from_attributes": True}

# -----------------------------------------------------
# ASSESSMENTS SCHEMAS
# -----------------------------------------------------

class AssessmentCreate(BaseModel):
    resume_id: int
    details: Optional[str] = None


class AssessmentRead(AssessmentCreate):
    id: int
    score: int

    model_config = {"from_attributes": True}

# -----------------------------------------------------
# SOFT SKIL QUESTIONS SCHEMAS
# -----------------------------------------------------

# --- Question Read ---
class SoftSkillQuestionRead(BaseModel):
    id: int
    question_text: str
    context: Optional[str]
    options: List[str]               # ["Agree","Neutral","Disagree"]
    weights: Dict[str, Dict[str, int]]  # { "Agree": {domain:weight}, ... }
    sort_order: int

    model_config = {"from_attributes": True}


# --- Questions page ---
class SoftSkillQuestionPage(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[SoftSkillQuestionRead]
    
    

class SoftSkillAnswerItem(BaseModel):
    question_id: int
    answer: str  # "Agree" / "Neutral" / "Disagree"


class SoftSkillAnswerBatchIn(BaseModel):
    session_id: str
    answers: List[SoftSkillAnswerItem]
    

class SoftSkillResultRead(BaseModel):
    session_id: str
    result: Dict[str, int]    # { "Engineering": 6, "Science & Research": 4, ... }
    completed_at: datetime

    model_config = {"from_attributes": True}



# -----------------------------------------------------
# TECHNICAL QUESTIONS SCHEMAS
# -----------------------------------------------------


class TechnicalDomainRead(BaseModel):
    id: int
    domain_name: str
    tree: Dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}
