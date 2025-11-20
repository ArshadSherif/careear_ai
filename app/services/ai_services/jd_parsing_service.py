from app.ai.gemini_client import run_json_prompt
import json

PROMPT = """
Your task is to convert a Job Description (JD) into STRICT NUMERIC VECTORS.

You MUST output ONLY the following JSON structure:

{
  "required_skills": { dynamic_skill_name: 0–1, ... },
  "jd_traits": { dynamic_trait_name: 0–1, ... },
  "jd_domains": { dynamic_domain_name: 0–1, ... },
  "jd_seniority": 0–1
}

DETAILED RULES:

1. **Dynamic Keys Allowed**
   - You may generate ANY number of skills, traits, or domain names.
   - Keys MUST come from the JD text meaningfully.
   - Keys MUST be short canonical names (e.g., “python”, “project_management”, “cloud”, “healthcare”).

2. **Numeric Output (0–1 only)**
   - Every skill, trait, and domain MUST have an importance score between 0 and 1.
   - Never output null, empty dicts, strings, or booleans.
   - If something is barely implied, give a small number (e.g., 0.1).

3. **What to Extract**
   - “required_skills”: tools, technologies, methods, knowledge areas.
   - “jd_traits”: behavioral indicators derived from verbs and adjectives (e.g., attention to detail).
   - “jd_domains”: the job-category taxonomy (e.g., AI, finance, healthcare, engineering, education).
   - “jd_seniority”: based on responsibilities (0 = intern/junior, 1 = senior/lead).

4. **Output Format Strictness**
   - JSON only.
   - No explanations.
   - No commentary.

JD TEXT:
<<<JD>>>
"""



def parse_jd_vectors(text: str) -> dict:
    prompt = PROMPT.replace("<<<JD>>>", text)
    raw = run_json_prompt(prompt)
    return json.loads(raw)
