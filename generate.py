import yaml
from pathlib import Path
from datetime import date
from typing import Any, Dict, List


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_MD = BASE_DIR / "resume.md"


# =========================
# YAML loaders（型安全）
# =========================
def load_yaml_list(path: Path, key: str) -> List[Any]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def load_yaml_dict(path: Path, key: str) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    value = data.get(key, {})
    return value if isinstance(value, dict) else {}


# =========================
# Load data
# =========================
career_list = load_yaml_list(DATA_DIR / "career.yaml", "career")
works_list = load_yaml_list(DATA_DIR / "works.yaml", "works")
skills_list = load_yaml_list(DATA_DIR / "skills.yaml", "skills")
languages = load_yaml_list(DATA_DIR / "languages.yaml", "languages")
strengths = load_yaml_list(DATA_DIR / "strengths.yaml", "strengths")
self_pr = load_yaml_dict(DATA_DIR / "self_pr.yaml", "self_pr")
profile = load_yaml_dict(DATA_DIR / "profile.yaml", "profile")


lines: List[str] = []


# =========================
# Helper
# =========================
def bullet_cell(items: Any, bullet: str) -> str:
    if not items:
        return ""

    if isinstance(items, str):
        items = [items]

    return r"\raw{openxml}{<w:br/>}".join(f"{bullet}{item}" for item in items)


# =========================
# タイトル
# =========================
lines.append(f"# {profile.get('title', '職務経歴書')}\n\n")

if profile.get("date") == "auto":
    today = date.today().strftime("%Y年%-m月%-d日現在")
    lines.append(f"{today}\n\n")

if profile.get("name"):
    lines.append(f"氏名　{profile['name']}\n\n")


# =========================
# 職務要約
# =========================
lines.append("## 職務要約\n\n")
lines.append(f"{profile.get('summary', '')}\n\n")


# =========================
# 職務経歴（会社 → 案件）
# =========================
lines.append("## 職務経歴\n\n")

for company in career_list:
    lines.append(f"### {company.get('company', '')}(在籍期間: {company.get('period', '')})\n\n")
    lines.append(f"事業内容：{company.get('industry', '')}　")
    lines.append(f"資本金：{company.get('capital', '')}　")
    lines.append(f"売上高：{company.get('revenue', '')} 　")
    lines.append(f"従業員数：{company.get('employees', '')}  \n\n")

    lines.append("| 期間 | 業務内容 |\n")
    lines.append("|---|---|\n")

    for project in company.get("projects", []):

        rows = [
            (project.get("period"), project.get('department', '')),
            (" ", f'**概要**：{project.get("summary")}'),
            (" ", f'**規模**：{project.get("scale")}'),
            (" ", f'**役割**：{project.get("role")}'),
            (" ", f'**OS**：{project.get("os")}'),
            (" ", "**担当フェーズ**"),
            (" ", f'{bullet_cell(project.get("phases"), "・")}'),
            (" ", "**主な業務**"),
            (" ", f'{bullet_cell(project.get("tasks"), "・")}'),
            (" ", f'**使用技術**：{project.get("tech")}'),
        ]

        for label, value in rows:
            if value:
                lines.append(f"| {label} | {value} |\n")


# =========================
# テクニカルスキル
# =========================
lines.append("## テクニカルスキル\n\n")
lines.append("| カテゴリ | スキル | 使用期間 | レベル |\n")
lines.append("|---|---|---|---|\n")

for block in skills_list:
    for i, item in enumerate(block.get("items", [])):
        category = block.get("category", "") if i == 0 else ""
        lines.append(
            f"| {category} | "
            f"{item.get('name','')} | "
            f"{item.get('period','')} | "
            f"{item.get('level','')} |\n"
        )

lines.append("\n")


# =========================
# 語学
# =========================
lines.append("## 語学\n\n")
lines.append("| 言語 | 習熟度 | 資格 / 補足 |\n")
lines.append("|---|---|---|\n")

for lang in languages:
    lines.append(
        f"| {lang.get('name','')} | "
        f"{lang.get('proficiency','')} | "
        f"{lang.get('details','')} |\n"
    )

lines.append("\n")


# =========================
# 活かせる経験・知識・技術
# =========================
lines.append("## 活かせる経験・知識・技術\n\n")
for item in strengths:
    lines.append(f"- {item}\n")
lines.append("\n")


# =========================
# 業務外での開発
# =========================
lines.append("## 業務外での開発\n\n")

lines.append("| タイトル | 内容 |\n")
lines.append("|---|---|\n")

for work in works_list:

    lines.append(f"| {work.get('title','')} | **概要**：{work.get('description','')} |\n")

    if work.get('period'):
        lines.append(f"|  | **制作期間**：{work.get('period')} |\n")

    if work.get('frontend'):
        lines.append(f"|  | **フロントエンド**：{work.get('frontend')} |\n")

    if work.get('backend') and work.get('backend') != []:
        lines.append(f"|  | **バックエンド**：{work.get('backend')} |\n")

    if work.get('tools') and work.get('tools') != []:
        lines.append(f"|  | **使用ツール**：{work.get('tools')} |\n")

    if work.get('urls') and work.get('urls') != []:
        lines.append(f"|  | **URL**：{bullet_cell(work.get('urls'), '・')} |\n")


# =========================
# 自己PR
# =========================
lines.append("## 自己PR\n\n")

for section in self_pr["about_me"]:
    body = section.get('body', '').replace('\n', '  \n')
    lines.append(f"{body}\n\n")


# =========================
# Write file
# =========================
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("resume.md generated successfully.")