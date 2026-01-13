import yaml
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_YAML = DATA_DIR / "cover_en.yaml"
OUTPUT_MD = BASE_DIR / "cover_letter.md"

def main():
    with open(INPUT_YAML, encoding="utf-8") as f:
        cover = yaml.safe_load(f)["cover"]

    lines = []

    # Header
    lines.append(f"# Cover Letter\n\n")
    lines.append(f"**Position:** {cover['position']}  \n")
    lines.append(f"**Company:** {cover['company']}\n\n")

    # Body
    lines.append(f"{cover['opening']}\n\n")
    lines.append(f"{cover['why_me']}\n\n")

    for exp in cover.get("experience", []):
        lines.append(f"- {exp}\n\n")
    lines.append("\n")

    lines.append(f"{cover.get('closing')}\n\n")
    lines.append(
        f"\nSincerely,\n\nUtano Kurihara\n{date.today():%B %d, %Y}\n"
    )

    OUTPUT_MD.write_text("".join(lines), encoding="utf-8")

    print("cover_letter.md generated successfully.")

if __name__ == "__main__":
    main()