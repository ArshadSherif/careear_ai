CAREER_PATH_RULES = {
    "data_scientist": ["python", "pandas", "numpy", "scikit-learn", "ml"],
    "backend_engineer": ["python", "fastapi", "sql", "docker", "kubernetes"],
    "devops_engineer": ["docker", "kubernetes", "terraform", "aws"]
}
def recommend_paths(skills: list[str]) -> list[str]:
    scored = []
    for path, reqs in CAREER_PATH_RULES.items():
        score = sum(1 for r in reqs if r in skills)
        if score:
            scored.append((path, score))
    scored.sort(key=lambda x: -x[1])
    return [p for p,_ in scored]
