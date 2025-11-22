from app.ai.gemini_client import run_json_prompt
import json

PROMPT = """
You are a strict domain scorer.

You must evaluate ALL domains from this approved list:
<<<DOMAIN_LIST>>>

Inputs:
resume_domains:
<<<RESUME_DOMAINS>>>

jd_domains:
<<<JD_DOMAINS>>>

soft_skill_domains:
<<<SOFT_DOMAINS>>>

Output format (strict JSON):
{
  "scores": {
      "<domain1>": <float>,
      "<domain2>": <float>,
      ...
  }
}

Rules:
- Include ALL domains from <<<DOMAIN_LIST>>>.
- Scores must be numeric.
- No explanations.
- No missing or extra keys.
- Never invent domains.
"""

def classify_domain_ai(
    resume_domains: dict,
    jd_domains: dict,
    soft_domains: dict,
    domain_list: list[str]
) -> dict:
    prompt = (
        PROMPT
        .replace("<<<DOMAIN_LIST>>>", json.dumps(domain_list))
        .replace("<<<RESUME_DOMAINS>>>", json.dumps(resume_domains))
        .replace("<<<JD_DOMAINS>>>", json.dumps(jd_domains))
        .replace("<<<SOFT_DOMAINS>>>", json.dumps(soft_domains))
    )

    raw = run_json_prompt(prompt)
    data = json.loads(raw)

    return data["scores"]       # dict of {domain: score}

