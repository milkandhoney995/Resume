import yaml
from pathlib import Path
from datetime import date
from typing import Any, Dict, List
import sys


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Language selection
LANGUAGE = sys.argv[1] if len(sys.argv) > 1 else "ja"
OUTPUT_MD = BASE_DIR / f"resume_{LANGUAGE}.md"


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
def get_data_filename(base_name: str) -> str:
    return f"{base_name}_en.yaml" if LANGUAGE == "en" else f"{base_name}.yaml"

career_list = load_yaml_list(DATA_DIR / get_data_filename("career"), "career")
works_list = load_yaml_list(DATA_DIR / get_data_filename("works"), "works")
skills_list = load_yaml_list(DATA_DIR / get_data_filename("skills"), "skills")
languages = load_yaml_list(DATA_DIR / get_data_filename("languages"), "languages")
strengths = load_yaml_list(DATA_DIR / get_data_filename("strengths"), "strengths")
self_pr = load_yaml_dict(DATA_DIR / get_data_filename("self_pr"), "self_pr")
profile = load_yaml_dict(DATA_DIR / get_data_filename("profile"), "profile")


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
# ヘッダー
# =========================
if LANGUAGE == "ja":
    lines.append(f"# {profile.get('title', '職務経歴書')}\n\n")

    if profile.get("date") == "auto":
        today = date.today().strftime("%Y年%-m月%-d日現在")
        lines.append(f"{today}\n\n")

    if profile.get("name"):
        lines.append(f"氏名　{profile['name']}\n\n")

else:
    # Name
    if profile.get("name"):
        lines.append(f"# {profile['name']}\n")

    # Headline
    if profile.get("headline"):
        lines.append(f"{profile['headline']}\n\n")

    # Contact info
    if profile.get("email"):
        lines.append(f"Email: {profile['email']}\n\n")

    if profile.get("github"):
        lines.append(f"GitHub: {profile['github']}\n\n")

    if profile.get("portfolio"):
        lines.append(f"Portfolio: {profile['portfolio']}\n")

    lines.append("\n")


# =========================
# 職務要約
# =========================
if LANGUAGE == "ja":
    lines.append("## 職務要約\n\n")
else:
    lines.append("## Professional Summary\n\n")
lines.append(f"{profile.get('summary', '')}\n\n")


# =========================
# 職務経歴（会社 → 案件）
# =========================
if LANGUAGE == "ja":
    lines.append("## 職務経歴\n\n")
else:
    lines.append("## Work Experience\n\n")

for company in career_list:
    lines.append(f"### {company.get('company', '')}({company.get('period', '')})\n\n")
    if LANGUAGE == "ja":
        lines.append(f"事業内容：{company.get('industry', '')}　")
        lines.append(f"資本金：{company.get('capital', '')}　")
        lines.append(f"売上高：{company.get('revenue', '')} 　")
        lines.append(f"従業員数：{company.get('employees', '')}  \n\n")

        lines.append("| 期間 | 業務内容 |\n")
        lines.append("|---|---|\n")
    else:

        pass

    for project in company.get("projects", []):
        if LANGUAGE == "ja":

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

        else:
            lines.append(f"{project.get('role','')} – {project.get('summary','')}\n\n")
            for task in project.get("tasks", []):
                lines.append(f"- {task}\n")
            if project.get("tech"):
                lines.append(f"- **Tech stack**: {project['tech']}\n")

            lines.append("\n")

# =========================
# テクニカルスキル
# =========================
if LANGUAGE == "ja":
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
else:
    lines.append("## Technical Skills\n\n")

    for block in skills_list:
        category = block.get("category", "")
        items = block.get("items", [])

        if not category or not items:
            continue

        skill_names = [
            item.get("name", "")
            for item in items
            if item.get("name")
        ]

        if skill_names:
            lines.append(
                f"{category}: {', '.join(skill_names)}\n\n"
            )

lines.append("\n")


# =========================
# 語学
# =========================
if LANGUAGE == "ja":
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

else:
    lines.append("## Languages\n\n")

    # proficiency ごとに言語をまとめる
    grouped = {}

    for lang in languages:
        name = lang.get("name")
        proficiency = lang.get("proficiency")
        details = lang.get("details")

        if not name or not proficiency:
            continue

        grouped.setdefault(proficiency, []).append({
            "name": name,
            "details": details
        })

    for proficiency, items in grouped.items():
        names = [item["name"] for item in items]

        # 資格は1つだけ付ける（通常は English）
        details_list = [
            item["details"]
            for item in items
            if item.get("details")
        ]

        line = f"{' / '.join(names)}: {proficiency}"

        if details_list:
            line += f" ({', '.join(details_list)})"

        lines.append(f"{line}\n\n")

    lines.append("\n")

# =========================
# 活かせる経験・知識・技術
# =========================
if LANGUAGE == "ja":
    lines.append("## 活かせる経験・知識・技術\n\n")
    for item in strengths:
        lines.append(f"- {item}\n")
else:
    pass

lines.append("\n")


# =========================
# 業務外での開発
# =========================
if LANGUAGE == "ja":
    lines.append("## 業務外での開発\n\n")
    lines.append("| タイトル | 内容 |\n")
    lines.append("|---|---|\n")

    for work in works_list:

        lines.append(f"| {work.get('title','')} | **概要**：{work.get('description','')} |\n" if LANGUAGE == "ja" else f"| {work.get('title','')} | **Overview**: {work.get('description','')} |\n")

        if work.get('period'):
            lines.append(f"|  | **制作期間**：{work.get('period')} |\n" if LANGUAGE == "ja" else f"|  | **Development Period**: {work.get('period')} |\n")

        if work.get('frontend'):
            lines.append(f"|  | **フロントエンド**：{work.get('frontend')} |\n" if LANGUAGE == "ja" else f"|  | **Frontend**: {work.get('frontend')} |\n")

        if work.get('backend') and work.get('backend') != []:
            lines.append(f"|  | **バックエンド**：{work.get('backend')} |\n" if LANGUAGE == "ja" else f"|  | **Backend**: {work.get('backend')} |\n")

        if work.get('tools') and work.get('tools') != []:
            lines.append(f"|  | **使用ツール**：{work.get('tools')} |\n" if LANGUAGE == "ja" else f"|  | **Tools Used**: {work.get('tools')} |\n")

        if work.get('urls') and work.get('urls') != []:
            lines.append(f"|  | **URL**：{bullet_cell(work.get('urls'), '・')} |\n" if LANGUAGE == "ja" else f"|  | **URL**: {bullet_cell(work.get('urls'), '・')} |\n")

else:
    lines.append("## Personal Projects\n\n")

    for work in works_list:
        title = work.get("title", "")
        description = work.get("description", "")
        urls = work.get("urls", [])

        if not title or not description:
            continue

        lines.append(
            f"{title} – {description}\n\n"
        )

        lines.append("\n")

# =========================
# 自己PR
# =========================
if LANGUAGE == "ja":
    lines.append("## 自己PR\n\n")
    for section in self_pr["about_me"]:
        body = section.get('body', '').replace('\n', '  \n')
        lines.append(f"{body}\n\n")
else:
    pass


# =========================
# Write file
# =========================
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"resume_{LANGUAGE}.md generated successfully.")