import sys
import requests
from bs4 import BeautifulSoup
from jd_parser import parse_jd
from jd_matcher import build_cover_yaml

url = sys.argv[1]

html = requests.get(url, timeout=10).text
soup = BeautifulSoup(html, "html.parser")

jd_data = parse_jd(soup)
cover_yaml = build_cover_yaml(jd_data)

with open("data/cover_en.yaml", "w", encoding="utf-8") as f:
    f.write(cover_yaml)

print("cover_en.yaml generated from job description.")