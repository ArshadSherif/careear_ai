import re, json
from pathlib import Path
from typing import List
SKILLS_FILE = Path(__file__).resolve().parents[1] / "assets" / "skills.json"
try:
    SKILLS = set(json.loads(SKILLS_FILE.read_text(encoding="utf8")).get("skills", []))
    SKILLS = {s.lower() for s in SKILLS}
except Exception:
    SKILLS = {"python", "sql", "fastapi", "docker", "aws"}
def extract_skills(text: str) -> List[str]:
    text = (text or "").lower()
    found = []
    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)
    return sorted(found)
