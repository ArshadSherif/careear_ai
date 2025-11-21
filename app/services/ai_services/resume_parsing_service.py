from app.ai.gemini_client import run_json_prompt
import json

PROMPT = """
You must extract skills, traits, domains, and experience from resume text.

Scoring rules:
- 1.0 = explicitly mentioned or strongly evidenced
- 0.5 = implicitly suggested or weak evidence
- 0.0 = not present

Output JSON:
{
  "skills": { "SkillName": score, ... },
  "traits": { "TraitName": score, ... },
  "domains": { "DomainName": score, ... },
  "experience": { "ExperienceItem": score, ... }
}


Resume text:
<<<RESUME>>>
"""

def parse_resume_vectors(text: str) -> dict:
    prompt = PROMPT.replace("<<<RESUME>>>", text)
    raw = run_json_prompt(prompt)
    return json.loads(raw)
