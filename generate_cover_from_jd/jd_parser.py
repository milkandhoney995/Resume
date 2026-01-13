import re
import yaml
from pathlib import Path

def parse_jd(soup):
    text = soup.get_text(separator="\n")

    return {
        "company": extract_company(text),
        "position": extract_position(text),
        "skills": extract_skills(text),
        "sections": extract_sections(text),
    }


def extract_company(text):
    patterns = [
        r"at\s+([A-Z][A-Za-z0-9 &]+)",
        r"join\s+([A-Z][A-Za-z0-9 &]+)",
        r"About\s+([A-Z][A-Za-z0-9 &]+)",
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group(1)

    return "Target Company"


def extract_position(text):
    title_candidates = [
        "Frontend Engineer",
        "Software Engineer",
        "Senior Frontend Engineer",
        "Web Engineer",
    ]

    for title in title_candidates:
        if title.lower() in text.lower():
            return title

    return "Frontend Engineer"


def extract_skills(text):
    with open(Path(__file__).parent.parent / "data" / "skill_keywords.yaml") as f:
        keywords = yaml.safe_load(f)["skills"]

    found = []
    lower_text = text.lower()

    for k in keywords:
        if k.lower() in lower_text:
            found.append(k)

    return found

def extract_sections(text):
    sections = {
        "responsibilities": [],
        "requirements": [],
    }

    current = None

    for line in text.splitlines():
        l = line.lower().strip()

        if "responsibilit" in l:
            current = "responsibilities"
            continue
        if "requirement" in l or "qualification" in l:
            current = "requirements"
            continue

        if current and line.strip():
            sections[current].append(line.strip())

    return sections