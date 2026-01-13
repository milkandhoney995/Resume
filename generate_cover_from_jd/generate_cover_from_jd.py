import sys
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from jd_parser import fetch_jd_html, parse_jd
from jd_matcher import build_llm_input
from llm_cover_generator import generate_cover_yaml

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "data" / "cover_en.yaml"

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_cover_from_jd.py <JOB_URL>")
        sys.exit(1)

    url = sys.argv[1]

    soup = fetch_jd_html(url)
    jd = parse_jd(soup)
    llm_input = build_llm_input(jd)

    cover_yaml = generate_cover_yaml(llm_input)

    OUTPUT.write_text(cover_yaml, encoding="utf-8")
    print("✅ cover_en.yaml generated successfully.")


if __name__ == "__main__":
    main()