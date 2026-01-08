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

# ===== 職務経歴 =====
lines.append("## 職務経歴\n\n")

for job in career_list:
    lines.append(f"### {job.get('period', '')}　{job.get('company', '')}\n\n")

    if job.get("employment"):
        lines.append(f"**雇用形態**  \n{job['employment']}\n\n")

    if job.get("department"):
        lines.append(f"**配属**  \n{job['department']}\n\n")

    if job.get("summary"):
        lines.append(f"**概要**  \n{job['summary']}\n\n")

    if job.get("phases"):
        lines.append("**担当フェーズ**\n")
        for p in job["phases"]:
            lines.append(f"- {p}\n")
        lines.append("\n")

    if job.get("tasks"):
        lines.append("**主な業務**\n")
        for t in job["tasks"]:
            lines.append(f"- {t}\n")
        lines.append("\n")

    if job.get("achievements"):
        lines.append("**実績・取り組み**\n")
        for a in job["achievements"]:
            lines.append(f"- {a}\n")
        lines.append("\n")

    if job.get("tech"):
        lines.append("**使用技術**\n")
        for tech in job["tech"]:
            lines.append(f"- {tech}\n")
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

    if work.get("period"):
        lines.append(f"**制作期間**  \n{work['period']}\n\n")

    if work.get("description"):
        lines.append(f"**概要**  \n{work['description']}\n\n")

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