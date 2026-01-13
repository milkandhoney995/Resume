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