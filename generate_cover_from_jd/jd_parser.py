# jd_parser.py

import re

def parse_jd(soup):
    text = soup.get_text(separator="\n")

    return {
        "company": extract_company(text),
        "position": extract_position(text),
        "skills": extract_skills(text),
    }


def extract_company(text):
    # 超シンプル（後で精度UP可能）
    return "Target Company"


def extract_position(text):
    patterns = [
        r"Frontend Engineer",
        r"Software Engineer",
        r"Web Engineer",
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return p
    return "Frontend Engineer"


def extract_skills(text):
    keywords = [
        "React", "Vue", "Next.js", "TypeScript",
        "JavaScript", "HTML", "CSS",
        "Auth0", "REST", "GraphQL"
    ]
    return [k for k in keywords if k.lower() in text.lower()]