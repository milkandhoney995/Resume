import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_yaml(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_llm_input(jd):
    profile = load_yaml("profile_en.yaml")["profile"]

    return {
        "candidate": {
            "name": profile["name"],
            "role": profile.get("role", "Frontend Engineer"),
            "summary": profile.get("summary", ""),
            "skills": profile.get("skills", []),
        },
        "job": {
            "company": jd["company"],
            "position": jd["position"],
            "responsibilities": jd["sections"]["responsibilities"],
            "requirements": jd["sections"]["requirements"],
            "tech_stack": jd["sections"]["tech_stack"],
        },
    }


def build_cover_yaml(jd):
    profile = load_yaml("profile_en.yaml")["profile"]
    career = load_yaml("career_en.yaml")["career"]

    opening = (
        f"I am writing to apply for the {jd['position']} position at {jd['company']}. "
        "I am excited about the opportunity to contribute to your team."
    )

    why_me = (
        "I am a frontend engineer with over 5 years of experience building "
        "scalable web applications using React, Vue, and Next.js."
    )

    experiences = []

    for company in career:
        for project in company.get("projects", []):
            for skill in jd["skills"]:
                if skill in project.get("tech", ""):
                    experiences.append(
                        f"At {company['company']}, I worked on {project.get('summary','')} "
                        f"using {skill}."
                    )

    experiences = experiences[:2] or [
        "I have consistently delivered frontend features in collaborative team environments."
    ]

    closing = (
        "I would welcome the opportunity to discuss how my skills and experience "
        "could contribute to your team. Thank you for your consideration."
    )

    return format_yaml(
        jd["company"],
        jd["position"],
        opening,
        why_me,
        experiences,
        closing,
    )


def format_yaml(company, position, opening, why_me, experiences, closing):
    exp_block = "\n".join(
        [f"    - >\n      {e}" for e in experiences]
    )

    return f"""cover:
  company: {company}
  position: {position}
  opening: >
    {opening}
  why_me: >
    {why_me}
  experience:
{exp_block}
  closing: >
    {closing}
"""