import re
import requests
from bs4 import BeautifulSoup
import yaml
from pathlib import Path

SECTION_HEADERS = {
    "summary": [
        "about the role", "job description", "overview"
    ],
    "responsibilities": [
        "responsibilities", "what you will do", "your role"
    ],
    "requirements": [
        "requirements", "qualifications", "what you bring", "must have"
    ],
    "preferred": [
        "preferred", "nice to have", "bonus", "plus"
    ],
    "tech_stack": [
        "tech stack", "technologies", "tools"
    ],
    "culture": [
        "culture", "values", "why join", "working at"
    ],
}

def fetch_jd_html(url: str) -> BeautifulSoup:
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def soup_to_lines(soup):
    lines = []

    for tag in soup.find_all(["h1", "h2", "h3", "li", "p"]):
        text = tag.get_text(strip=True)
        if len(text.split()) >= 3:
            lines.append(text)

    return lines

def extract_sections(soup):
    lines = soup_to_lines(soup)
    sections = {k: [] for k in SECTION_HEADERS}
    current = None

    for line in lines:
        n = normalize(line)

        for section, headers in SECTION_HEADERS.items():
            if any(h in n for h in headers):
                current = section
                break
        else:
            if current:
                sections[current].append(line)

    return sections

def extract_company(text: str) -> str:
    match = re.search(r"at\s+([A-Z][A-Za-z0-9 &]+)", text)
    return match.group(1) if match else "Target Company"

def extract_position(text: str) -> str:
    for title in [
        "Frontend Engineer",
        "Senior Frontend Engineer",
        "Software Engineer",
        "Web Engineer",
    ]:
        if title.lower() in text.lower():
            return title
    return "Frontend Engineer"

def parse_jd(soup):
    text = soup.get_text(separator="\n")
    return {
        "company": extract_company(text),
        "position": extract_position(text),
        "sections": extract_sections(soup),
    }


def extract_skills(text):
    with open(Path(__file__).parent.parent / "data" / "skill_keywords.yaml") as f:
        keywords = yaml.safe_load(f)["skills"]

    found = []
    lower_text = text.lower()

    for k in keywords:
        if k.lower() in lower_text:
            found.append(k)

    return found
