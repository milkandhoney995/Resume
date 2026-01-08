from docx import Document
from pathlib import Path

path = Path("職務経歴書.docx")

if not path.exists():
    raise FileNotFoundError(
        f"{path} が見つかりません。build.sh を先に実行してください。"
    )

doc = Document(str(path))

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text = cell.text
            if "・" in text:
                cell.text = ""
                p = cell.paragraphs[0]
                for line in text.split("・"):
                    if line.strip():
                        run = p.add_run("・" + line.strip())
                        run.add_break()  # Shift+Enter 相当

doc.save(str(path))