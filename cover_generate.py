import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_MD = BASE_DIR / "cover_letter_en.md"

with open(DATA_DIR / "cover_en.yaml", encoding="utf-8") as f:
    data = yaml.safe_load(f)

cover = data["cover"]

lines = []

# Header
lines.append(f"{cover.get('position')} Application\n\n")

# Body
lines.append(f"{cover.get('opening')}\n\n")
lines.append(f"{cover.get('why_me')}\n\n")

for exp in cover.get("experience", []):
    lines.append(f"{exp}\n\n")

lines.append(f"{cover.get('closing')}\n\n")
lines.append("Sincerely,\n\nUtano Kurihara\n")

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("cover_letter_en.md generated.")