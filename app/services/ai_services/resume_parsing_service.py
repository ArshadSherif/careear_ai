from app.ai.gemini_client import run_json_prompt
import json

PROMPT = """
You receive extracted resume text.
You must output ONLY strict JSON with the following fields:

{
  "skills": {...},
  "traits": {...},
  "domains": {...},
  "experience": {...}
}

Rules:
- No narrative.
- No subjective text.
- Only numeric values between 0 and 1.
- Keep field names EXACT.
- Do not include any additional fields.

Resume text:
<<<RESUME>>>
"""

def parse_resume_vectors(text: str) -> dict:
    prompt = PROMPT.replace("<<<RESUME>>>", text)
    raw = run_json_prompt(prompt)
    return json.loads(raw)
