from app.ai.gemini_client import run_json_prompt
import json


PROMPT = """
You are a strict domain classifier.

You must choose ONE domain from this approved list:
<<<DOMAIN_LIST>>>

You are given three inputs:

resume_domains:
<<<RESUME_DOMAINS>>>

jd_domains:
<<<JD_DOMAINS>>>

soft_skill_domains:
<<<SOFT_DOMAINS>>>

Rules:
- You must output ONLY strict JSON:
{
  "domain": "<one_exact_domain_from_list>"
}
- No explanation.
- No extra keys.
- Never invent domain names.
- The domain MUST be exactly one of the items from <<<DOMAIN_LIST>>>.
"""

def classify_domain_ai(
    resume_domains: dict,
    jd_domains: dict,
    soft_domains: dict,
    domain_list: list[str]
) -> str:
    prompt = (
        PROMPT
        .replace("<<<DOMAIN_LIST>>>", json.dumps(domain_list))
        .replace("<<<RESUME_DOMAINS>>>", json.dumps(resume_domains))
        .replace("<<<JD_DOMAINS>>>", json.dumps(jd_domains))
        .replace("<<<SOFT_DOMAINS>>>", json.dumps(soft_domains))
    )

    raw = run_json_prompt(prompt)
    data = json.loads(raw)
    return data["domain"]
