import yaml
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_MD = BASE_DIR / "resume.md"


def load_yaml(path, key):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get(key, [])


career_list = load_yaml(DATA_DIR / "career.yaml", "career")
works_list = load_yaml(DATA_DIR / "works.yaml", "works")
skills_list = load_yaml(DATA_DIR / "skills.yaml", "skills")
profile = load_yaml(DATA_DIR / "profile.yaml", "profile")
profile = profile[0] if isinstance(profile, list) else profile

lines = []

# ===== タイトル =====
lines.append(f"# {profile.get('title', '職務経歴書')}\n\n")

if profile.get("date") == "auto":
    today = date.today().strftime("%Y年%-m月%-d日現在")
    lines.append(f"{today}\n\n")

if profile.get("name"):
    lines.append(f"氏名　{profile['name']}\n\n")

# ===== 職務要約 =====
lines.append("## 職務要約\n\n")
lines.append(
    "フロントエンドエンジニアとして、React / Vue / Next.js を中心とした\n"
    "Webアプリケーションの設計・実装に従事。\n"
    "UI/UX設計から実装、テストまで一貫して対応可能。\n"
    "業務外でも継続的に個人開発を行い、技術力の向上に努めている。\n\n"
)

# ===== 職務経歴（会社 → 案件 ネスト表） =====
lines.append("## 職務経歴\n\n")

def bullet_list(items):
    if not items:
        return ""

    if isinstance(items, str):
        items = [items]

    return r"\raw{openxml}{<w:br/>}".join(f"・{item}" for item in items)

for company in career_list:
    lines.append(f"### {company.get('company', '')}\n\n")

    if company.get("employment"):
        lines.append(f"**雇用形態**：{company['employment']}  \n")
    if company.get("period"):
        lines.append(f"**在籍期間**：{company['period']}\n\n")

    for project in company.get("projects", []):
        lines.append(f"#### 【案件】{project.get('name', '')}\n\n")

        lines.append("| 項目 | 内容 |\n")
        lines.append("|---|---|\n")

        rows = [
            ("期間", project.get("period")),
            ("規模", project.get("scale")),
            ("役割", project.get("role")),
            ("OS", project.get("os")),
            ("概要", project.get("summary")),
            ("担当フェーズ", bullet_list(project.get("phases"))),
            ("主な業務", bullet_list(project.get("tasks"))),
            ("使用技術", bullet_list(project.get("tech"))),
        ]

        for label, value in rows:
            if value:
                lines.append(f"| {label} | {value} |\n")

        lines.append("\n")

# ===== テクニカルスキル =====
lines.append("## テクニカルスキル\n\n")

for block in skills_list:
    lines.append(f"### {block.get('category', '')}\n\n")

    # Markdownテーブル
    lines.append("| スキル | 使用期間 | レベル |\n")
    lines.append("|---|---|---|\n")

    for item in block.get("items", []):
        name = item.get("name", "")
        period = item.get("period", "")
        level = item.get("level", "")
        lines.append(f"| {name} | {period} | {level} |\n")

    lines.append("\n")

# ===== 業務外での開発 =====
lines.append("## 業務外での開発\n\n")

for work in works_list:
    lines.append(f"### {work.get('title', '')}\n\n")

    if work.get("description"):
        lines.append(f"**概要**：{work['description']}\n\n")

    if work.get("period"):
        lines.append(f"**制作期間**{work['period']}\n\n")

    if work.get("frontend"):
        lines.append("**フロントエンド**\n")
        for f in work["frontend"]:
            lines.append(f"- {f}\n")
        lines.append("\n")

    if work.get("backend"):
        lines.append("**バックエンド**\n")
        for b in work["backend"]:
            lines.append(f"- {b}\n")
        lines.append("\n")

    if work.get("tools"):
        lines.append("**使用ツール**\n")
        for t in work["tools"]:
            lines.append(f"- {t}\n")
        lines.append("\n")

    if work.get("urls"):
        lines.append("**URL**\n")
        for u in work["urls"]:
            lines.append(f"- {u}\n")
        lines.append("\n")

# ===== 書き込み =====
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("resume.md generated successfully.")